from django.urls import path
from . import views
from .views import MenuDetailView, MenuListView, AddToCartView, ViewCartView, ClearCartView, RemoveFromCartView
from .controller import cart

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', MenuListView.as_view(), name='menu'),
    path('menu/<int:pk>', MenuDetailView.as_view(), name='menu-detail'),
    path('add-to-cart/', cart.addtocart,  name='add-to-cart'),
    path('view-cart/', cart.viewcart,  name='view-cart'),
    path('update-cart/', cart.updatecart,  name='update-cart'),
    path('remove-item/', cart.removeitem,  name='remove-item'),
    path('clear-cart/', ClearCartView.as_view(), name='clear-cart'),
    path('remove-from-cart/<int:pk>/', RemoveFromCartView.as_view(), name='remove-from-cart')
]
