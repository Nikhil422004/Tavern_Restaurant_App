from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .forms import SearchForm
from .models import Menu, Cart

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
        cart_items = Cart.objects.filter(user=self.request.user)
        context['cartItems'] = cart_items
        return context

class MenuDetailView(LoginRequiredMixin, DetailView):
    model = Menu
    template_name = "menu/menu_detail.html"
    context_object_name = "menu"

def about(request):
    return render(request, 'menu/about.html', {'title': 'About'})
