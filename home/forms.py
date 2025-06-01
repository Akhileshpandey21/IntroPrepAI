from django import forms
from .models import ImageUpload
from .models import Review

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['title', 'image']




class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'role', 'rating', 'text']
