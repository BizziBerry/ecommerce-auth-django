'''from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .token_utils import account_activation_token

def send_activation_email(request, user):
    """Отправка email для активации аккаунта"""
    current_site = get_current_site(request)
    subject = _('Активация аккаунта на {}').format(current_site.name)
    
    # Создание ссылки подтверждения
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    activation_link = f"http://{current_site.domain}/accounts/activate/{uid}/{token}/"

    # Рендер HTML и текстового сообщения
    html_message = render_to_string('accounts/email/activation_email.html', {
        'user': user,
        'activation_link': activation_link,
        'domain': current_site.domain,
        'site_name': current_site.name,
    })
    
    text_message = render_to_string('accounts/email/activation_email.txt', {
        'user': user,
        'activation_link': activation_link,
        'domain': current_site.domain,
        'site_name': current_site.name,
    })

    try:
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False

def send_password_reset_email(user, reset_url):
    """Отправка email для сброса пароля"""
    subject = _('Сброс пароля на ShopShield Pro')
    
    html_message = render_to_string('accounts/email/password_reset_email.html', {
        'user': user,
        'reset_url': reset_url,
    })
    
    text_message = render_to_string('accounts/email/password_reset_email.txt', {
        'user': user,
        'reset_url': reset_url,
    })

    try:
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False'''

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .token_utils import account_activation_token

def send_activation_email(request, user):
    """Отправка email для активации аккаунта"""
    try:
        current_site = get_current_site(request)
        subject = _('Активация аккаунта на ShopShield Pro')
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = f"http://{current_site.domain}/accounts/activate/{uid}/{token}/"

        # HTML сообщение
        html_message = render_to_string('accounts/email/activation_email.html', {
            'user': user,
            'activation_link': activation_link,
            'domain': current_site.domain,
            'site_name': current_site.name,
        })
        
        # Текстовое сообщение
        text_message = render_to_string('accounts/email/activation_email.txt', {
            'user': user,
            'activation_link': activation_link,
            'domain': current_site.domain,
            'site_name': current_site.name,
        })

        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False

def send_password_reset_email(user, reset_url):
    """Отправка email для сброса пароля"""
    subject = _('Сброс пароля на ShopShield Pro')
    
    html_message = render_to_string('accounts/email/password_reset_email.html', {
        'user': user,
        'reset_url': reset_url,
    })
    
    text_message = render_to_string('accounts/email/password_reset_email.txt', {
        'user': user,
        'reset_url': reset_url,
    })

    try:
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False