from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django import forms
from django.db.models import Q
from .forms import CreateForm
from .consts import ITEM_PER_PAGE
from .models import Book, Review

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
    for book in object_list:
        book.category_disp = CATEGORY_DICT.get(book.category, book.category)
    for book in ranking_list:
        book.category_disp = CATEGORY_DICT.get(book.category, book.category)

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
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.book.id})



def search_view(request):
    query = request.GET.get('query', '')  # GETパラメータからクエリを取得
    books = Book.objects.all()

    if query:
        # タイトルまたは説明に検索ワードが含まれる場合にフィルタリング
        books = books.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )

    context = {
        'books': books,
        'query': query,
    }
    return render(request, 'book/search.html', context)