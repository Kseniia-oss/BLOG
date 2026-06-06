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
        # Перейменували на 'current_category', як просить шаблон викладача
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
        "categories": Category.objects.all() # щоб меню працювало і на сторінці посту
    }
    return render(request, "main/post_detail.html", context)


def product_list(request):
    products = Product.objects.all()
    return render(request, 'main/product_list.html', {'products': products})