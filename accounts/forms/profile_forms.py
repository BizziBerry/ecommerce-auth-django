'''from django import forms
from django.utils.translation import gettext_lazy as _
from ..models import CustomUser

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        disabled=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        label=_('Email (нельзя изменить)')
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
            'rows': 4
        }),
        label=_('Адрес доставки')
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'address')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Проверка уникальности, исключая текущего пользователя
            if CustomUser.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(_('Пользователь с таким номером телефона уже существует.'))
        return phone_number

class AccountDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label=_('Я понимаю, что все мои данные будут удалены без возможности восстановления')
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите ваш пароль для подтверждения')
        }),
        label=_('Текущий пароль'),
        help_text=_('Введите ваш текущий пароль для подтверждения удаления аккаунта')
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError(_('Неверный пароль.'))
        return password '''
    
from django import forms
from django.utils.translation import gettext_lazy as _
from ..models import CustomUser

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        disabled=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        label=_('Email')
    )
    phone_number = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('+7 XXX XXX-XX-XX')
        }),
        label=_('Номер телефона')
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _('Ваш адрес доставки'),
            'rows': 4
        }),
        label=_('Адрес доставки')
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'address')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Проверка уникальности, исключая текущего пользователя
            if CustomUser.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(_('Пользователь с таким номером телефона уже существует.'))
        return phone_number

class AccountDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label=_('Я понимаю, что все мои данные будут удалены без возможности восстановления')
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите ваш пароль для подтверждения')
        }),
        label=_('Текущий пароль'),
        help_text=_('Введите ваш текущий пароль для подтверждения удаления аккаунта')
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError(_('Неверный пароль.'))
        return password
    