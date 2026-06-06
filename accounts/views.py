from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from main.models import Category

def register_view(request):
    if request.user.is_authenticated:
        return redirect('main:post_list')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:post_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Реєстрація'})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:post_list')
        
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:post_list')
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form, 'title': 'Вхід'})

def logout_view(request):
    logout(request)
    return redirect('main:post_list')

@login_required(login_url='accounts:login')
def profile_view(request):
    context = {
        'title': f'Профіль {request.user.username}',
        'categories': Category.objects.all()  # Передаємо для бічного чи верхнього меню
    }
    return render(request, 'accounts/profile.html', context)