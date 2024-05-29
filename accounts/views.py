from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .forms import CustomUserChangeForm
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .models import CustomUser
from django.shortcuts import render, get_object_or_404



def public_users_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'accounts/user_public_detail.html', {'user': user})




class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

from django.urls import reverse_lazy

class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'accounts/user_update.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('accounts:user_detail', kwargs={'pk': self.object.pk})


from django.views.generic import DetailView

class UserDetailView(LoginRequiredMixin, DetailView):
    form_class = CustomUserChangeForm
    template_name = 'accounts/user_detail.html'
    def get_object(self):
        return self.request.user


class Logout(LogoutView):
    template_name = 'accounts/logout.html'

class UserPublicDetailView(DetailView):
    model = CustomUser
    template_name = 'accounts/user_public_detail.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(CustomUser, username=username)