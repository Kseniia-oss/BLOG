from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse  

class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Слаг для URL")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=[self.slug])


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
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name="products", 
        verbose_name="Категорія"
    )
    name = models.CharField(max_length=100, verbose_name="Назва товару")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Слаг для URL")
    description = models.TextField(verbose_name="Опис товару")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Зображення")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    views = models.IntegerField(default=0, verbose_name="Кількість переглядів")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    is_active = models.BooleanField(default=True, verbose_name="У наявності")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return f"{self.name} ({self.created_at.strftime('%d.%m.%Y')})"
    
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.id, self.slug])