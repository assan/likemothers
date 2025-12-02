# shop/models.py
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('ЧПУ (латиницей)', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'          # ← будет в меню
        ordering = ['name']


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    name = models.CharField('Название товара', max_length=200)
    slug = models.SlugField('ЧПУ (латиницей)', unique=True)
    image = models.ImageField('Фото', upload_to='products/', blank=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена (₸)', max_digits=10, decimal_places=0)
    weight = models.IntegerField('Вес (грамм)')
    available = models.BooleanField('В продаже', default=True)
    stock = models.PositiveIntegerField('Остаток на складе', default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'             # ← будет в меню
        ordering = ['name']