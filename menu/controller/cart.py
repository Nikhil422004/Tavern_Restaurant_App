from django.shortcuts import redirect, render
from django.contrib import messages
from django.http.response import JsonResponse
from menu.models import Menu, Cart

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