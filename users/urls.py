from django.urls import path
from . import views
from .views import RegisterUser, ThanksForRegister
app_name = 'users'  # Пространство имен для приложения

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('signup/', RegisterUser.as_view(), name='signup'),
    path('thanks/', ThanksForRegister.as_view(), name='thanks'),  # URL для страницы благодарности
    ]
