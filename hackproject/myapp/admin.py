from django.contrib import admin

# Register your models here.
from .models import FoodItem  # or whatever your model is called
from .models import Review

admin.site.register(FoodItem)
admin.site.register(Review)
