from django.shortcuts import redirect, render
from django.contrib import messages
from django.http.response import JsonResponse
from django.utils.dateparse import parse_datetime
from menu.models import Menu, Cart
import json

def addtocart(request):
    if request.method == 'POST':
        menuId = int(request.POST.get('menuId'))
        menuCheck = Menu.objects.get(pk=menuId)
        if menuCheck:
            if(Cart.objects.filter(user=request.user.id, menu=menuCheck)):
                messages.success(request, f'Item already in cart')
                return JsonResponse({'status': 'Item already in cart'})
            else:
                print(Cart.objects.filter(user=request.user.id, pk=menuId))
                menuQty = int(request.POST.get('menuQty')) 
                Cart.objects.create(user=request.user, menu=menuCheck, menuQty=menuQty)
                messages.success(request, f'Item has been added to cart')
                return JsonResponse({'status': 'Item added to cart successfully'})

        else:
            return JsonResponse({'status': 'No such Item'})
    
    return redirect('/menu')

def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    cart_items = Cart.objects.filter(user=request.user)
    total_cost = sum(item.menu.price * item.menuQty for item in cart_items)
    context = {
        'cart':cart,
        'total_cost':total_cost
    }
    return render(request, 'menu/view_cart.html', context)

def updatecart(request):
    if request.method == 'POST':
        menuId = int(request.POST.get('menuId'))
        menuCheck = Menu.objects.get(pk=menuId)
        cart = Cart.objects.get(user=request.user.id, menu=menuCheck)
        if(cart):
            menuQty = int(request.POST.get('menuQty'))
            cart.menuQty = menuQty
            cart.save()

            cart_items = Cart.objects.filter(user=request.user)
            total_cost = sum(item.menu.price * item.menuQty for item in cart_items)

            return JsonResponse({'status': 'Updated successfully', 'total_cost': total_cost})
    return redirect('update-cart/')
        

def removeitem(request):
    if request.method == 'POST':
        menuId = int(request.POST.get('menuId'))
        menuCheck = Menu.objects.get(pk=menuId)
        cart = Cart.objects.get(user=request.user.id, menu=menuCheck)
        if(cart):
            cart.delete()
            messages.error(request, f'Item has been removed from cart')

            cart_items = Cart.objects.filter(user=request.user)
            total_cost = sum(item.menu.price * item.menuQty for item in cart_items)

            return JsonResponse({'status': 'Removed Item', 'total_cost': total_cost})
    return redirect('remove-item/')

def clearcart(request):
    cart = Cart.objects.filter(user=request.user)
    cart.delete()
    return redirect('view-cart/')


def confirmorder(request):
    cart = Cart.objects.filter(user=request.user)
    if request.method == 'POST':
        new_order = request.user.profile.add_order(cart)
        cart.delete()

        messages.success(request, "Order confirmed successfully!")
        return redirect('confirmation-page', order_id=new_order['order_id'])

def confirmation_page(request, order_id):
    orders = json.loads(request.user.profile.orders)
    order = next(order for order in orders if order['order_id'] == order_id)
    order['date_posted'] = parse_datetime(order['date_posted'])

    context = {
        'order': order,
    }
    return render(request, 'menu/confirmation.html', context)
