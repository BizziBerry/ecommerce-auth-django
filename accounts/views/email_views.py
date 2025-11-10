from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib import messages
from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from ..models import CustomUser
from ..utils.token_utils import account_activation_token

@csrf_protect
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if user.is_active:
            messages.warning(request, _('Ваш аккаунт уже был активирован ранее.'))
        else:
            user.is_active = True
            user.is_verified = True
            user.save()
            messages.success(request, _('Ваш email успешно подтвержден! Теперь вы можете войти в систему.'))
        
        return redirect('accounts:login')
    else:
        return render(request, 'accounts/email/activation_invalid.html')