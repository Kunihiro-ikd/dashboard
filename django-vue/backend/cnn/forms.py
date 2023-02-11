from django import forms
from .models import UploadImage
from .widgets import FileInputWithPreview
from .models import Document

# html の form で使用
class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['title', 'image']

        widgets = {
            'file': FileInputWithPreview,
            # 次のようにすると、プレビューエレメントがウィジェットに含まれない。つまりプレビューエレメントを自分で好きな場所にかける
            # 'file': FileInputWithPreview(include_preview=False)
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )




