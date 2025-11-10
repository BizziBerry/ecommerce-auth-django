from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import json

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_('Пользователь')
    )
    session_key = models.CharField(
        max_length=40, 
        blank=True, 
        null=True,
        verbose_name=_('Ключ сессии')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создана'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Обновлена'))

    class Meta:
        verbose_name = _('Корзина')
        verbose_name_plural = _('Корзины')

    def __str__(self):
        return f"Корзина {self.user.email}"

    @property
    def total_items(self):
        return self.items.count()

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def clear(self):
        """Очистка корзины"""
        self.items.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Корзина')
    )
    product_id = models.PositiveIntegerField(verbose_name=_('ID товара'))
    product_name = models.CharField(max_length=255, verbose_name=_('Название товара'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Количество'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Добавлен'))

    class Meta:
        verbose_name = _('Элемент корзины')
        verbose_name_plural = _('Элементы корзины')
        unique_together = ['cart', 'product_id']
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.price

    def to_dict(self):
        """Преобразование в словарь для сессии"""
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'price': float(self.price),
        }

class CartManager:
    """Менеджер для работы с корзиной"""
    
    @staticmethod
    def get_or_create_cart(request):
        """Получение или создание корзины для пользователя/сессии"""
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            return cart
        else:
            # Для анонимных пользователей используем сессию
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            
            # Создаем временную корзину в сессии
            if 'cart' not in request.session:
                request.session['cart'] = {}
            
            return None

    @staticmethod
    def merge_carts(request, user):
        """Объединение сессионной корзины с корзиной пользователя"""
        if 'cart' in request.session and request.session['cart']:
            cart, created = Cart.objects.get_or_create(user=user)
            session_cart = request.session['cart']
            
            for product_id, item_data in session_cart.items():
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    product_id=product_id,
                    defaults={
                        'product_name': item_data['product_name'],
                        'quantity': item_data['quantity'],
                        'price': item_data['price'],
                    }
                )
                if not created:
                    cart_item.quantity += item_data['quantity']
                    cart_item.save()
            
            # Очищаем сессионную корзину
            del request.session['cart']
            request.session.modified = True