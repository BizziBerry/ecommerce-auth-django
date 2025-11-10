from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Email подтверждение
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activation-sent/', views.email_confirmation_sent, name='activation_sent'),
    
    # Профиль
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_update, name='profile_edit'),
    path('profile/security/', views.password_change, name='security'),
    path('profile/delete/', views.account_delete, name='delete_account'),
    
    # Сброс пароля
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/auth/password_reset.html',
             email_template_name='accounts/email/password_reset_email.html',
             subject_template_name='accounts/email/password_reset_subject.txt',
             success_url='/accounts/password-reset/done/'
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/auth/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/auth/password_reset_confirm.html',
             success_url='/accounts/reset/done/'
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/auth/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]