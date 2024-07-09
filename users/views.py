from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
import json

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You will now be able to log in. ')
            return redirect('login')
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')


    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    orders = json.loads(request.user.profile.orders)
    for order in orders:
        order['date_posted'] = parse_datetime(order['date_posted'])

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'orders': orders,
    }

    return render(request, 'users/profile.html', context)

def delete_order(request, order_id):
    if request.method == 'POST':
        request.user.profile.delete_order(order_id)
        messages.success(request, 'Order has been deleted.')
        return redirect('profile')