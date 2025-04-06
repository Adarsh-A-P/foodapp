from django import forms
from .models import FoodItem, Review
from django.utils import timezone

class FoodItemForm(forms.ModelForm):
    location_link = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Paste your location link (e.g., Google Maps link)'
        })
    )
    
    class Meta:
        model = FoodItem
        fields = ['title', 'description', 'quantity', 'food_type', 'expiry_date', 'location', 'location_link', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter food item title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the food item'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2 kg, 3 boxes'}),
            'food_type': forms.Select(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pickup location description'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date and expiry_date < timezone.now():
            raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry_date

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review here'})
        }