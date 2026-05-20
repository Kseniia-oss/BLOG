from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.post_list, name="post_list"),
    path('products/', views.product_list, name="product_list"),  # Сторінка товарів
]