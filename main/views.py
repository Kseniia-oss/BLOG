from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from .models import Post, Category, Product

class PostListView(ListView):
    model = Post
    template_name = "main/post_list.html"
    context_object_name = "posts"
    allow_empty = True
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get("category_slug")

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        sort = self.request.GET.get('sort')

        if sort == 'new':
            queryset = queryset.order_by('-created_at')
        elif sort == 'old':
            queryset = queryset.order_by('created_at')
        elif sort == 'popular':
            queryset = queryset.order_by('-views')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home page"
        context["categories"] = Category.objects.all()
        context["current_category"] = Category.objects.filter(slug=self.kwargs.get("category_slug")).first()
        return context


def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    post.views += 1
    post.save()
    
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:4]
    
    context = {
        "title": post.title,
        "post": post,
        "related_posts": related_posts,
        "categories": Category.objects.all()
    }
    return render(request, "main/post_detail.html", context)


def product_list(request, category_slug=None):
    # Беремо лише активні товари
    products = Product.objects.filter(is_active=True)
    
    # Фільтрація за категорією, якщо вона передана в URL маршруту
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
    
    # Отримуємо параметр сортування з GET-запиту
    sort = request.GET.get('sort')

    if sort == 'new':
        products = products.order_by('-created_at')
    elif sort == 'old':
        products = products.order_by('created_at')
    elif sort == 'popular':
        products = products.order_by('-views')
    elif sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        # Сортування за замовчуванням
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'current_sort': sort or 'new',
        'categories': Category.objects.all(),  # Для коректного відображення категорій у меню base.html
        'current_category': current_category   # Передаємо для підсвічування активного пункту в меню
    }
    return render(request, 'main/product_list.html', context)


def product_detail(request, id, slug):
    # Отримуємо товар або повертаємо 404
    product = get_object_or_404(Product, id=id, slug=slug)
    
    # Збільшуємо лічильник переглядів та зберігаємо в БД
    product.views += 1
    product.save()
    
    # Знаходимо схожі товари (з тієї ж категорії, крім поточного, ліміт 4)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    
    context = {
        "title": product.name,
        "product": product,
        "related_products": related_products,
        "categories": Category.objects.all()
    }
    return render(request, "main/product_detail.html", context)