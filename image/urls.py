from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('image/', views.ListImageView.as_view(), name='list-image'),
    path('image/<int:pk>/detail/', views.DetailImageView.as_view(), name='detail-image'),
    path('image/create/', views.CreateImageView.as_view(), name='create-image'),
    path('image/<int:pk>/delete/', views.DeleteImageView.as_view(), name='delete-image'),
    path('image/<int:pk>/update/', views.UpdateImageView.as_view(), name='update-image'),
    path('image/<int:image_id>/review/', views.CreateReviewView.as_view(), name='review'),
    path('image/search/', views.search_view, name='search'),
]