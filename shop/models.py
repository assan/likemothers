from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='products/', blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)  # в тенге
    weight = models.IntegerField(help_text="в граммах")
    available = models.BooleanField(default=True)

    # ←←← НОВОЕ ПОЛЕ
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])