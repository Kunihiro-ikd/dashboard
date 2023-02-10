from django import forms
from .models import UploadImage

# html の form で使用
class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['image']


