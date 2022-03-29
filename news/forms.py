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
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'input-textbox input-textbox', 'rows': "10", 'cols': "50",
                                          'placeholder': 'Commenting publicly'}),
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 5000:
            return text
        raise ValidationError('Max comment size is 5000 characters')


class LikeForm(forms.Form):
    like = forms.BooleanField(required=False,
                              widget=forms.CheckboxInput(attrs={'onclick': 'this.form.submit();',
                                                                'class': 'checkbox like'}))

    def __init__(self, article: News, user: Profile, *args, **kwargs):
        updated_initial = dict()
        updated_initial['like'] = self.is_liked(article, user)
        kwargs.update(initial=updated_initial)
        super(LikeForm, self).__init__(*args, **kwargs)

    def is_liked(self, article: News, user: Profile):
        if user in article.users_who_liked.all():
            return True
        return False
