from .auth_views import register, custom_login, email_confirmation_sent
from .email_views import activate
from .profile_views import profile, profile_update, password_change, account_delete

__all__ = [
    'register',
    'custom_login', 
    'email_confirmation_sent',
    'activate',
    'profile',
    'profile_update', 
    'password_change',
    'account_delete',
]