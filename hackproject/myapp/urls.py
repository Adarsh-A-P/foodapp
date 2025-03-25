from django.urls import path
from . import views
from .views import review_section

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

]