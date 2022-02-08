from django import forms
from django.core.exceptions import ValidationError

from .models import News, NewsComments


class AddingNewsForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = "Unknown"
        self.fields['author'].initial = user
    
    class Meta:
        model = News
        fields = ['title', 'author', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-textbox'}),
            'author': forms.Select(attrs={'class': 'input-textbox'}),
            'text': forms.Textarea(attrs={'class': 'input-textbox input-textbox-90', 'rows': "10", 'cols': "50"}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.istitle():
            return title
        raise ValidationError('All words in a title start with a upper case letter,'
                              ' and the rest of the word are lower case letter')


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
        title = self.cleaned_data['title']
        title = title.strip()

        if title[0].isalnum():
            title = title[0].upper() + title[1:]
            return title
        raise ValidationError('The first word must start with a letter or number.')

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 1000:
            return text
        raise ValidationError('Max comment size is 1000 characters')
