from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField, \
    PasswordResetForm, SetPasswordForm
from django_registration.forms import RegistrationForm

from .models import Profile


class ProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Profile
        fields = ('username', 'email')


class ProfileChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ('username', 'email')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'input-textbox', 'placeholder': 'Enter your email', 'id': 'email'}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-textbox',
                'placeholder': 'Enter your password',
                'id': 'password',
                'autocomplete': 'current-password',
            })
    )


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'input-textbox',
            'autocomplete': 'email',
            'placeholder': 'Enter your email',
        })
    )


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-textbox',
            'placeholder': 'Enter new password',
            'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'input-textbox',
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password'}),
    )


User = get_user_model()


class MyCustomUserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = Profile
        fields = (
            'username',
            User.get_email_field_name(),
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'input-textbox',
            'autocomplete': 'username',
            'placeholder': 'Enter your or company name',
        })
    )

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'input-textbox',
            'autocomplete': 'email',
            'placeholder': 'Enter your email',
        })
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-textbox',
                'placeholder': 'Enter your password',
                'id': 'password',
                'autocomplete': 'current-password',
            })
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-textbox',
                'placeholder': 'Enter your password',
                'id': 'password',
                'autocomplete': 'current-password',
            })
    )