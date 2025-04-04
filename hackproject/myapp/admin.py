from django.contrib import admin
from .models import FoodItem, Review

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'quantity', 'food_type', 'expiry_date', 'location']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'date_posted']
