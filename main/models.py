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
        # Змінено на product_list_by_category згідно з ТЗ для фільтрації товарів
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
    # ДОДАНО: Зв'язок «один до багатьох» з Категорією
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name="products", 
        verbose_name="Категорія"
    )
    name = models.CharField(max_length=100, verbose_name="Назва товару")
    # ДОДАНО: Унікальний слаг для URL товару
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Слаг для URL")
    description = models.TextField(verbose_name="Опис товару")
    # ДОДАНО: Поле для завантаження зображення товару
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Зображення")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    # ДОДАНО: Кількість переглядів
    views = models.IntegerField(default=0, verbose_name="Кількість переглядів")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    is_active = models.BooleanField(default=True, verbose_name="У наявності")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    # ЗМІНЕНО: Тепер виводить назву товару та дату його створення
    def __str__(self):
        return f"{self.name} ({self.created_at.strftime('%d.%m.%Y')})"
    
    # ДОДАНО: Генерація динамічного посилання на детальну сторінку товару
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.id, self.slug])