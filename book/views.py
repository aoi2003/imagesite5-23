from django.contrib.auth.mixins import LoginRequiredMixin  #ログインしていないユーザーを特定のページにリダイレクトするという仕様を簡単に実装できるようになる。
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Avg, Q #Djangoではfilter()でDBのレコードを検索することができます。
#その時にOR検索や否定条件を指定したい時があります。そういう時はQオブジェクトを使うと簡単にできます。
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django import forms
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Book, Like, Review
from .forms import CreateForm
from .consts import ITEM_PER_PAGE


CATEGORY_DICT = {
    'kawaii': 'かわいい',
    'cool': 'かっこいい', 
    'other': 'その他',
}




class ListBookView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/book_list.html'
    paginate_by = ITEM_PER_PAGE


class DetailBookView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    


class CreateBookView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'book/book_create.html'
    form_class = CreateForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteBookView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'book/book_delete.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied

        return obj


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'text', 'category', 'thumbnail')
        labels = {
            'title': 'タイトル',
            'text': 'テキスト',
            'category': 'カテゴリ',
            'thumbnail': '投稿画像',
        }

class UpdateBookView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookUpdateForm
    template_name = 'book/book_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied

        return obj

    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.id})

def index_view(request):
    object_list = Book.objects.order_by('-id')
    ranking_list = Book.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')

    user = request.user
    paginator = Paginator(ranking_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

    return render(
        request,
        'book/index.html',
        {
            'object_list': object_list,
            'ranking_list': ranking_list,
            'page_obj': page_obj,
            'user': request.user,
        }
    )


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'book/review_form.html'
    fields = ('book',  'text', 'rate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        return context
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book_id = self.kwargs['book_id']  # この行を追加
        return super().form_valid(form)



def search_view(request):
    query = request.GET.get('query', '')  # GETパラメータからクエリを取得
    books = Book.objects.all()

    if query:
        # タイトルまたは説明に検索ワードが含まれる場合にフィルタリング
        books = books.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )   #Qオブジェクトを使うと、SQLのWHERE句に相当する条件を、Pythonのコード内で簡潔かつ読みやすく記述することができます。
            #特に複数の条件を組み合わせる場合に便利です。

    context = {
        'books': books,
        'query': query,
    }
    return render(request, 'book/search.html', context)

