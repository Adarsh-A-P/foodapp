from django.urls import path
from . import views
from .views import review_section

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('search/', views.search_food, name='search_food'),
    path('add/', views.add_food_item, name='add_food_item'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('reviews/', review_section, name='review_section'),
    path('food/<int:food_id>/', views.food_detail, name='food_detail'),
    path('food/<int:food_id>/edit/', views.edit_food_item, name='edit_food_item'),
    path('food/<int:food_id>/delete/', views.delete_food_item, name='delete_food_item'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),  # Changed from cart/add/<int:product_id>/
    path('api/cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('api/cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
]