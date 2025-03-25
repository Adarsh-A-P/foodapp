from django import forms
from .models import FoodItem
from django.utils import timezone

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['title', 'description', 'quantity', 'food_type', 'expiry_date', 'location', 'image']
        widgets = {
            'expiry_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date and expiry_date < timezone.now():
            raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry_date

from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']    