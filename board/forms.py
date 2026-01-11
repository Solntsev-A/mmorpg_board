from django import forms
from .models import Response


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
