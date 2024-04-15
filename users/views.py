from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginUserForm, RegisterUserForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import TemplateView



class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('index')
    

class LogoutUser(LogoutView):
    next_page = reverse_lazy('users:login')




def signup_user(request):
    pass

class RegisterUser(LoginRequiredMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:thanks')  # Указываем новый URL для страницы благодарности

    def form_valid(self, form):
        response = super().form_valid(form)
        # Автоматически входим пользователя в систему после успешной регистрации
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            # Дополнительные действия после успешной регистрации, если необходимо
        return response

class ThanksForRegister(TemplateView):
    template_name = 'users/thanks.html'