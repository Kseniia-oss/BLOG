from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse  

class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="Ім'я категорії")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Слаг для url")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("main:post_list_by_category", args=[self.slug])


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='post_images/%Y/%m/%d', blank=True)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"

    def __str__(self):
        return f"{self.title} - {self.created_at}"
    
    def get_absolute_url(self):
        return reverse("main:post_detail", args=[self.id, self.slug])


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва товару")
    description = models.TextField(verbose_name="Опис товару")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    is_active = models.BooleanField(default=True, verbose_name="У наявності")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name