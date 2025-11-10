from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache

from ..forms import CustomUserCreationForm, CustomAuthenticationForm
from ..utils.email_utils import send_activation_email

@sensitive_post_parameters()
@csrf_protect
@never_cache
def register(request):
    if request.user.is_authenticated:
        messages.info(request, _('Вы уже авторизованы.'))
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Аккаунт не активен до подтверждения email
            user.save()

            # Отправка email для активации
            send_activation_email(request, user)
            
            messages.success(
                request, 
                _('Регистрация успешна! Проверьте вашу почту для подтверждения email.')
            )
            return redirect('accounts:activation_sent')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/auth/register.html', {'form': form})

@sensitive_post_parameters()
@csrf_protect
@never_cache
def custom_login(request):
    if request.user.is_authenticated:
        messages.info(request, _('Вы уже авторизованы.'))
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, _('Добро пожаловать, {}!').format(email))
                
                # Перенаправление на next параметр или профиль
                next_url = request.GET.get('next', 'accounts:profile')
                return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/auth/login.html', {'form': form})

def email_confirmation_sent(request):
    return render(request, 'accounts/email/activation_sent.html')