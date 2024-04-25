from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from pyexpat.errors import messages

from .forms import LoginUserForm, RegisterUserForm
from re import T
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileUserForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView
)
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm
)
from .forms import UserPasswordChangeForm
from django.views.generic import ListView
from cards.models import Card
from django.views.generic import TemplateView
class RegisterDone(TemplateView):
    template_name = 'users/register_done.html'
    extra_context = {'title': 'Регистрация завершена'}
    

class LogoutUser(LogoutView):
    next_page = reverse_lazy('users:login')

class RegisterUser(CreateView):
    form_class = RegisterUserForm  # Указываем класс формы, который мы создали для регистрации
    template_name = 'users/register.html'  # Путь к шаблону, который будет использоваться для отображения формы
    extra_context = {'title': 'Регистрация'}  # Дополнительный контекст для передачи в шаблон
    success_url = reverse_lazy('users:login')  # URL, на который будет перенаправлен пользователь после успешной регистрации

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
    
        next_url = self.request.POST.get('next', '').strip()
        if next_url:
            return next_url # Перенаправляем на next_url, если он был передан
        return reverse_lazy('catalog')
    

class LogoutUser(LogoutView):
    next_page = reverse_lazy('users:login')
    
class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()  # Используем модель текущего пользователя
    form_class = ProfileUserForm  # Связываем с формой профиля пользователя
    template_name = 'users/profile.html'  # Указываем путь к шаблону
    extra_context = {'title': 'Профиль пользователя',
                     'active_tab': 'profile'}  # Дополнительный контекст для передачи в шаблон

    def get_success_url(self):
        # URL, на который переадресуется пользователь после успешного обновления
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        # Возвращает объект модели, который должен быть отредактирован
        return self.request.user
    
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    extra_context = {'title': 'Изменение пароля',
                     'active_tab': 'password_change'}
    success_url = reverse_lazy('users:password_change_done')

    def form_valid(self, form):
        # Вызов метода form_valid родительского класса
        response = super().form_valid(form)

        # Дополнительная логика при успешной смене пароля
        # Например, отправка уведомления пользователю
        messages.success(self.request, 'Пароль успешно изменен.')

        return response



class UserPasswordChangeDone(TemplateView):
    template_name = 'users/password_change_done.html'
    extra_context = {'title': 'Пароль изменен успешно'}

class UserPasswordReset(PasswordResetView):
    template_name = 'users/password_reset_done.html'
    form_class = PasswordResetForm
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'reset_password_subject.txt'
    success_url = reverse_lazy('users:password_reset_confirm')
    def form_valid(self, form):
        # Вызываем родительский метод для обработки формы
        super_result = super().form_valid(form)

        # Дополнительные действия после успешной отправки формы
        user_email = form.cleaned_data['email']
        send_mail(
            'Запрос на сброс пароля получен',
            'Ваш запрос на сброс пароля успешно получен.',
            'from@example.com',
            [user_email],
            fail_silently=False,
        )

        return super_result
class PasswordResetDone(TemplateView):
    template_name = 'users/password_reset_done.html'
    extra_context = {'title': 'Инструкции отправлены'}

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('users:password_reset_complete')

    def form_valid(self, form):
        # Вызываем родительский метод для обработки формы
        super_result = super().form_valid(form)

        # Дополнительные действия после успешного сброса пароля
        user_email = self.request.user.email  # Предполагая, что у пользователя есть электронная почта
        send_mail(
            'Пароль успешно изменен',
            'Ваш пароль успешно изменен.',
            'from@example.com',
            [user_email],
            fail_silently=False,
        )

        return super_result
class PasswordResetComplete(TemplateView):
    template_name = 'password_reset_complete.html'
    extra_context = {'title': 'Пароль успешно обновлен'}
class UserCardsView(ListView):
    model = Card
    template_name = 'users/profile_cards.html'
    context_object_name = 'cards'
    extra_context = {'title': 'Мои карточки',
                     'active_tab': 'profile_cards'}
    def get_queryset(self):
        return Card.objects.filter(author=self.request.user).order_by('-upload_date')

def signup_user(request):
    pass

class RegisterUser(CreateView):
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