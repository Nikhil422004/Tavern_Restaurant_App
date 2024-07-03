from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
# Create your models here.

class Menu(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(default="menu/default.jpg", upload_to="menu")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("menu-detail", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height != 500 and img.width != 500:
            output_size = (500, 500)
            img = img.resize(output_size, Image.LANCZOS)
            img.save(self.image.path)