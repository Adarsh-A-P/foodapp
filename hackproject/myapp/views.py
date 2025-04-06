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
from django.http import JsonResponse
from .models import CartItem, Product
import json

# Home View
def home(request):
    food_items = FoodItem.objects.all().order_by('-date_posted')[:9]  # Get latest 9 items
    latest_reviews = Review.objects.all().order_by('-date_posted')[:3]
    
    context = {
        'food_items': food_items,
        'latest_reviews': latest_reviews,
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
            # In add_food_item view
            return redirect('myapp:home')
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
                # In login_view
                return redirect('myapp:home')
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
            # In signup_view
            return redirect('myapp:home')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})

# Logout View
@login_required
def logout_view(request):
    logout(request)
    # In logout_view
    return redirect('myapp:home')

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
            return redirect('myapp:review_section')  # Add namespace
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


@login_required
def edit_food_item(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)
    
    # Check if the user is the owner
    if request.user != food_item.user:
        return redirect('myapp:home')
    
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food_item)
        if form.is_valid():
            form.save()
            return redirect('myapp:food_detail', food_id=food_id)
    else:
        form = FoodItemForm(instance=food_item)
    
    return render(request, 'myapp/edit_food_item.html', {'form': form, 'food_item': food_item})

@login_required
def delete_food_item(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)
    
    # Check if the user is the owner
    if request.user != food_item.user:
        return redirect('myapp:home')
    
    if request.method == 'POST':
        food_item.delete()
        return redirect('myapp:home')
    
    return redirect('myapp:food_detail', food_id=food_id)


# Add these new cart-related views
@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'myapp/cart.html', context)

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            
            # Get or create the product
            product, created = Product.objects.get_or_create(
                id=product_id,
                defaults={
                    'name': data.get('name'),
                    'price': data.get('price'),
                    'unit': data.get('unit')
                }
            )
            
            # Get or create cart item
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': 1}
            )
            
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            
            cart_count = CartItem.objects.filter(user=request.user).count()
            
            return JsonResponse({
                'success': True,
                'cart_count': cart_count,
                'message': 'Item added to cart successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    cart_total = sum(item.product.price * item.quantity for item in CartItem.objects.filter(user=request.user))
    return JsonResponse({'success': True, 'cart_total': cart_total})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    
    cart_total = sum(item.product.price * item.quantity for item in CartItem.objects.filter(user=request.user))
    return JsonResponse({'success': True, 'cart_total': cart_total})

# Add this context processor function
def cart_count_processor(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0
    return {'cart_count': cart_count}


@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        # Handle form submission
        # Add your order processing logic here
        return redirect('myapp:order_confirmation')
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'myapp/checkout.html', context)