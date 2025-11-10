from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
import json

from .models import Cart, CartItem, CartManager

def cart_detail(request):
    """Детальная страница корзины"""
    cart = CartManager.get_or_create_cart(request)
    
    if request.user.is_authenticated and cart:
        items = cart.items.all()
        total_price = cart.total_price
        total_items = cart.total_items
    else:
        # Для анонимных пользователей
        session_cart = request.session.get('cart', {})
        items = []
        total_price = 0
        total_items = 0
        
        for product_id, item_data in session_cart.items():
            items.append({
                'product_id': product_id,
                'product_name': item_data['product_name'],
                'quantity': item_data['quantity'],
                'price': item_data['price'],
                'total_price': item_data['quantity'] * item_data['price'],
            })
            total_price += item_data['quantity'] * item_data['price']
            total_items += item_data['quantity']

    context = {
        'items': items,
        'total_price': total_price,
        'total_items': total_items,
    }
    return render(request, 'cart/cart.html', context)

def cart_add(request, product_id):
    """Добавление товара в корзину"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product_name = request.POST.get('product_name', f'Товар {product_id}')
        price = float(request.POST.get('price', 0))
        
        if request.user.is_authenticated:
            cart = CartManager.get_or_create_cart(request)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_id=product_id,
                defaults={
                    'product_name': product_name,
                    'quantity': quantity,
                    'price': price,
                }
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            messages.success(request, _('Товар добавлен в корзину!'))
        else:
            # Для анонимных пользователей
            if 'cart' not in request.session:
                request.session['cart'] = {}
            
            cart = request.session['cart']
            if str(product_id) in cart:
                cart[str(product_id)]['quantity'] += quantity
            else:
                cart[str(product_id)] = {
                    'product_name': product_name,
                    'quantity': quantity,
                    'price': price,
                }
            
            request.session.modified = True
            messages.success(request, _('Товар добавлен в корзину!'))

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Товар добавлен в корзину'})
        
        return redirect('cart:detail')
    
    return redirect('cart:detail')

def cart_remove(request, product_id):
    """Удаление товара из корзины"""
    if request.user.is_authenticated:
        cart = CartManager.get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()
        messages.success(request, _('Товар удален из корзины'))
    else:
        # Для анонимных пользователей
        if 'cart' in request.session and str(product_id) in request.session['cart']:
            del request.session['cart'][str(product_id)]
            request.session.modified = True
            messages.success(request, _('Товар удален из корзины'))

    return redirect('cart:detail')

def cart_update(request, product_id):
    """Обновление количества товара в корзине"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            return cart_remove(request, product_id)
        
        if request.user.is_authenticated:
            cart = CartManager.get_or_create_cart(request)
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            cart_item.quantity = quantity
            cart_item.save()
        else:
            # Для анонимных пользователей
            if 'cart' in request.session and str(product_id) in request.session['cart']:
                request.session['cart'][str(product_id)]['quantity'] = quantity
                request.session.modified = True

        messages.success(request, _('Корзина обновлена'))
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
    
    return redirect('cart:detail')

def cart_clear(request):
    """Очистка корзины"""
    if request.user.is_authenticated:
        cart = CartManager.get_or_create_cart(request)
        cart.clear()
    else:
        # Для анонимных пользователей
        if 'cart' in request.session:
            del request.session['cart']
            request.session.modified = True
    
    messages.success(request, _('Корзина очищена'))
    return redirect('cart:detail')