from django import forms
from django.core.exceptions import ValidationError

from service.services import get_choices_from_query
from users.models import Profile
from .models import News, NewsComments
from .services.services import get_clean_title


class AddingNewsForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = "Unknown"
        self.fields['author'].initial = user
        self.fields['author'].choices = get_choices_from_query(Profile, {"is_staff": "True"})
    
    class Meta:
        model = News
        fields = ['title', 'author', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-textbox'}),
            'author': forms.Select(attrs={'class': 'input-textbox'}),
            'text': forms.Textarea(attrs={'class': 'input-textbox input-textbox-90', 'rows': "10", 'cols': "50"}),
        }

    def clean_title(self):
        return get_clean_title(self.cleaned_data['title'])


class NewsCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = NewsComments
        fields = ['title', 'text', 'stars']
        CHOICES = (
            ('5', '5 stars - Excellent'),
            ('4', '4 stars - Very good'),
            ('3', '3 stars - Satisfactory'),
            ('2', '2 stars - Poor'),
            ('1', '1 star - Fail'),
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-textbox', 'placeholder': 'Title'}),
            'text': forms.Textarea(attrs={'class': 'input-textbox input-textbox-90', 'rows': "10", 'cols': "50",
                                          'placeholder': 'Commenting publicly'}),
            'stars': forms.Select(attrs={'class': 'input-textbox'}, choices=CHOICES),
        }

    def clean_title(self):
        return get_clean_title(self.cleaned_data['title'])

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 1000:
            return text
        raise ValidationError('Max comment size is 1000 characters')
