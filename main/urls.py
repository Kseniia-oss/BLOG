from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.PostListView.as_view(), name="post_list"),
    path('posts/<slug:category_slug>/', views.PostListView.as_view(), name="post_list_by_category"),
    path('post/<int:id>/<slug:slug>/', views.post_detail, name="post_detail"),
    
    path('products/', views.product_list, name="product_list"),
    path('products/<slug:category_slug>/', views.product_list, name="product_list_by_category"),
    
    path('product/<int:id>/<slug:slug>/', views.product_detail, name="product_detail"),
]