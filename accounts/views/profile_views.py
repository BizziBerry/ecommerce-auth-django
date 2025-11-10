from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from ..forms import ProfileUpdateForm, CustomPasswordChangeForm, AccountDeleteForm

@login_required
def profile(request):
    return render(request, 'accounts/profile/profile.html', {'user': request.user})

@login_required
@csrf_protect
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Ваш профиль успешно обновлен!'))
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile/profile_edit.html', {'form': form})

@login_required
@csrf_protect
def password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Ваш пароль успешно изменен!'))
            return redirect('accounts:profile')
        else:
            messages.error(request, _('Пожалуйста, исправьте ошибки в форме.'))
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'accounts/profile/security.html', {'form': form})

@login_required
@csrf_protect
def account_delete(request):
    if request.method == 'POST':
        form = AccountDeleteForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = request.user
            user_email = user.email
            user.delete()
            messages.success(
                request, 
                _('Аккаунт {} успешно удален.').format(user_email)
            )
            return redirect('home')
    else:
        form = AccountDeleteForm(user=request.user)
    
    return render(request, 'accounts/profile/account_delete.html', {'form': form})