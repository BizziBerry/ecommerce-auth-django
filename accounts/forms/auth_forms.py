from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from ..models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите ваш email'),
            'autocomplete': 'email'
        }),
        label=_('Email')
    )
    phone_number = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('+7 XXX XXX-XX-XX'),
            'autocomplete': 'tel'
        }),
        label=_('Номер телефона')
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _('Ваш адрес доставки'),
            'rows': 3
        }),
        label=_('Адрес доставки')
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Пароль'),
            'autocomplete': 'new-password'
        }),
        label=_('Пароль'),
        help_text=_('Пароль должен содержать минимум 8 символов')
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Подтверждение пароля'),
            'autocomplete': 'new-password'
        }),
        label=_('Подтверждение пароля')
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'address', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Пользователь с таким email уже существует.'))
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(_('Пользователь с таким номером телефона уже существует.'))
        return phone_number

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        return password1

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите ваш email'),
            'autocomplete': 'email'
        }),
        label=_('Email')
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Пароль'),
            'autocomplete': 'current-password'
        }),
        label=_('Пароль')
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _('Ваш аккаунт не активирован. Проверьте вашу почту для подтверждения.'),
                code='inactive',
            )
        super().confirm_login_allowed(user)

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Текущий пароль'),
            'autocomplete': 'current-password'
        }),
        label=_('Текущий пароль')
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Новый пароль'),
            'autocomplete': 'new-password'
        }),
        label=_('Новый пароль')
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Подтверждение нового пароля'),
            'autocomplete': 'new-password'
        }),
        label=_('Подтверждение нового пароля')
    )