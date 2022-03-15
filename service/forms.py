from django import forms
from django.core.exceptions import ValidationError

from news.services.services import get_clean_title
from .models import Orders, Services
from users.models import Profile
from .services import get_choices_from_query


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'input-textbox input-textbox-90', 'rows': "10", 'cols': "50"}),
        }


class KanbanSelectForm(forms.ModelForm):
    def __init__(self, order, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kanban_type'].initial = order.kanban_type

    class Meta:
        model = Orders
        fields = ['kanban_type']
        widgets = {
            'kanban_type': forms.Select(),
        }


class ExecutorSelectForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].choices = get_choices_from_query(Profile, {"is_staff": "True"})
        self.fields['executor'].initial = user

    class Meta:
        model = Orders
        fields = ['executor']
        widgets = {
            'executor': forms.Select(),
        }


class AddServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name', 'text', 'price', 'run_time']
        widgets = {
            'name': forms.TextInput(),
            'text': forms.Textarea(),
            'price': forms.TextInput(),
            'run_time': forms.TimeInput(),
        }

    def clean_name(self):
        return get_clean_title(self.cleaned_data['name'])
