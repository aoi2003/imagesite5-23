from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django import forms
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Image, Like, Review
from .forms import CreateForm
from .consts import ITEM_PER_PAGE

CATEGORY_DICT = {
    'kawaii': 'かわいい',
    'cool': 'かっこいい',
    'other': 'その他',
}

class ListImageView(LoginRequiredMixin, ListView):
    model = Image
    template_name = 'image/image_list.html'  # 変更
    paginate_by = ITEM_PER_PAGE

class DetailImageView(DetailView):
    model = Image
    template_name = 'image/image_detail.html'  # 変更

class CreateImageView(LoginRequiredMixin, CreateView):
    model = Image
    template_name = 'image/image_create.html'  # 変更
    form_class = CreateForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeleteImageView(LoginRequiredMixin, DeleteView):
    model = Image
    template_name = 'image/image_delete.html'  # 変更
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

class ImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'text', 'category', 'thumbnail')
        labels = {
            'title': 'タイトル',
            'text': 'テキスト',
            'category': 'カテゴリ',
            'thumbnail': '投稿画像',
        }

class UpdateImageView(LoginRequiredMixin, UpdateView):
    model = Image
    form_class = ImageUpdateForm
    template_name = 'image/image_update.html'  # 変更

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

    def get_success_url(self):
        return reverse('detail-image', kwargs={'pk': self.object.id})

def index_view(request):
    object_list = Image.objects.order_by('-id')
    ranking_list = Image.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')
    user = request.user
    paginator = Paginator(ranking_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

    return render(
        request,
        'image/index.html',  # 変更
        {
            'object_list': object_list,
            'ranking_list': ranking_list,
            'page_obj': page_obj,
            'user': request.user,
        }
    )

class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'image/review_form.html'
    fields = ('text', 'rate')  # image フィールドを削除

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = get_object_or_404(Image, pk=self.kwargs['image_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.image = get_object_or_404(Image, pk=self.kwargs['image_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail-image', kwargs={'pk': self.kwargs['image_id']})
        # 'detail-image' は画像の詳細ページのURLパターン名です。
        # 画像の詳細ページにリダイレクトするようにします。

def search_view(request):
    query = request.GET.get('query', '')
    images = Image.objects.all()

    if query:
        images = images.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        )

    context = {
        'images': images,
        'query': query,
    }
    return render(request, 'image/search.html', context)  # 変更