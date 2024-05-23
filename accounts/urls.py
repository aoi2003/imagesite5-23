from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import SignUpView, UserUpdateView, UserDetailView,Logout

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name="logout"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('users/update/', UserUpdateView.as_view(), name='user_update'),
    path('users/detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
]