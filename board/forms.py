from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Response, Advertisement


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите текст отклика...',
            })
        }


class AdvertisementForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = Advertisement
        fields = ['title', 'category', 'content']
