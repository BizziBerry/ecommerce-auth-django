from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name=_('Номер телефона'),
        help_text=_('Формат: +7 XXX XXX-XX-XX')
    )
    address = models.TextField(blank=True, verbose_name=_('Адрес доставки'))
    
    # Статусы
    is_active = models.BooleanField(default=False, verbose_name=_('Аккаунт активен'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Сотрудник'))
    is_verified = models.BooleanField(default=False, verbose_name=_('Email подтвержден'))
    
    # Даты
    date_joined = models.DateTimeField(default=timezone.now, verbose_name=_('Дата регистрации'))
    last_updated = models.DateTimeField(auto_now=True, verbose_name=_('Последнее обновление'))
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email.split('@')[0]

    @property
    def has_shipping_address(self):
        return bool(self.address.strip())

class EmailConfirmationToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() <= self.expires_at

    class Meta:
        verbose_name = _('Токен подтверждения email')
        verbose_name_plural = _('Токены подтверждения email')
