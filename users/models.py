from django.db import models
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
import json
import shortuuid

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    orders = models.TextField(default='[]')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def add_order(self, cart):
        orders = json.loads(self.orders)
        order_uuid = shortuuid.uuid()
        
        # Create a new order
        new_order = {
            'order_id': order_uuid,
            'items': [],
            'total_cost': 0.0,
            'date_posted': timezone.now().isoformat()
        }

        # Iterate through the cart items
        for cart_item in cart:
            menu = cart_item.menu
            quantity = cart_item.menuQty

            item = {
                'menu_id': menu.pk,
                'title': menu.title,
                'quantity': quantity,
                'price': float(menu.price),
            }
            
            new_order['items'].append(item)
            new_order['total_cost'] += float(menu.price) * quantity

        # Append the new order to the orders list
        orders.append(new_order)
        
        # Save the updated orders list back to the orders field
        self.orders = json.dumps(orders)
        self.save()
        return new_order 