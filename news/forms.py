from django import forms
from .models import News


class AddingNewsForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = "Unknown"
        self.fields['author'].initial = user
    
    class Meta:
        model = News
        fields = ['title', 'slug', 'author', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-textbox'}),
            'slug': forms.TextInput(attrs={'class': 'input-textbox'}),
            'author': forms.Select(attrs={'class': 'input-textbox'}),
            'text': forms.Textarea(attrs={'class': 'input-textbox input-textbox-90', 'rows': "10", 'cols': "50"}),
        }
