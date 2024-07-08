from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from .forms import SearchForm
from .models import Menu

# Create your views here.
def home(request):
    return render(request, 'menu/home.html', {'title': 'Home'})

class MenuListView(LoginRequiredMixin, ListView):
    model = Menu
    template_name = "menu/menu.html"
    context_object_name = "menuItems"
    form_class = SearchForm

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchForm(self.request.GET or None)
        context['form'] = form
        return context

class MenuDetailView(LoginRequiredMixin, DetailView):
    model = Menu
    template_name = "menu/menu_detail.html"
    context_object_name = "menu"

class AddToCartView(View):
    def get(self, request, pk):
        menuItem = get_object_or_404(Menu, pk=pk)
        cart = request.session.get('cart', [])
        cart.append({'id': menuItem.id, 'title': menuItem.title, 'price': str(menuItem.price)})
        request.session['cart'] = cart
        messages.success(request, f'Item has been added to cart')

        return redirect('menu')

class ViewCartView(View):
    def get(self, request):
        cart = request.session.get('cart',[])
        total_cost = sum(float(item['price']) for item in cart)
        return render(request, 'menu/view_cart.html', {'cart':cart, 'total_cost':total_cost})

class RemoveFromCartView(View):
    def post(self, request, pk):
        cart = request.session.get('cart', [])
        for index, item in enumerate(cart):
            if item['id'] == pk:
                del cart[index]
                break
        request.session['cart'] = cart
        messages.warning(request, f'Item has been removed from cart')
        return redirect('view-cart')
    
class ClearCartView(View):
    def get(self, request):
        request.session['cart'] = []
        messages.error(request, f'Your cart has been cleared.')
        return redirect('view-cart')


def about(request):
    return render(request, 'menu/about.html', {'title': 'About'})
