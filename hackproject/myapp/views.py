from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.utils import timezone
from .models import FoodItem, Review  # Import the Review model
from .forms import FoodItemForm, ReviewForm  # Import the ReviewForm
from .models import Review 
from django.shortcuts import render

# Home View
def home(request):
    food_items = FoodItem.objects.all().order_by('-date_posted')[:9]  # Get latest 9 items
    
    context = {
        'food_items': food_items,
        'latest_reviews': Review.objects.all().order_by('-date_posted')[:3]  # Example for reviews

    }
    return render(request, 'myapp/home.html', context)
    



# Search Food View
def search_food(request):
    query = request.GET.get('q')
    if query:
        food_items = FoodItem.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        )
    else:
        food_items = FoodItem.objects.none()
    return render(request, 'myapp/search_results.html', {'food_items': food_items, 'query': query})

# Add Food Item View
@login_required
def add_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.user = request.user
            food_item.save()
            return redirect('home')
    else:
        form = FoodItemForm()
    return render(request, 'myapp/add_food_item.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})

# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# About View
def about(request):
    return render(request, 'myapp/about.html')

# Review Section View
def review_section(request):
    reviews = Review.objects.all().order_by('-date_posted')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review_section')
    else:
        form = ReviewForm()
    return render(request, 'myapp/review_section.html', {'form': form, 'reviews': reviews})
@login_required
def review_section(request):
    reviews = Review.objects.all().order_by('-date_posted')
   
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review_section')
    else:
        form = ReviewForm()
    return render(request, 'myapp/review_section.html', {'form': form, 'reviews': reviews})
from django.shortcuts import render, get_object_or_404
from .models import FoodItem

def food_detail(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)
    context = {
        'food_item': food_item,
    }
    return render(request, 'myapp/food_detail.html', context)

def home(request):
    # Fetch the latest 3 reviews
    latest_reviews = Review.objects.all().order_by('-date_posted')[:3]
    
    context = {
        'latest_reviews': latest_reviews,
    }
    return render(request, 'myapp/home.html', context)