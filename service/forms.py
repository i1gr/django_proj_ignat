from django import forms
from django.core.exceptions import ValidationError

from .models import Orders
from users.models import Profile


class OrderForm(forms.ModelForm):
    # def __init__(self, user, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['customer'].empty_label = "Unknown"
    #     self.fields['customer'].initial = user

    class Meta:
        model = Orders
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'input-textbox input-textbox-90', 'rows': "10", 'cols': "50"}),
        }



