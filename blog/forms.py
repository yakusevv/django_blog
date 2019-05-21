import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Tag, Post, Profile


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        return new_slug


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('slug may not be "Create"')
        return new_slug


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
            ]
        help_texts = {
            'first_name': "Enter your name",
            'last_name': "Enter your last name"
        }


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
                'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                'last_name' : forms.TextInput(attrs={'class': 'form-control'}),
                'email'     : forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location', 'birth_date']
        widgets = {
                'avatar'     : forms.FileInput(attrs={
                                                'class': "form-control-file",
                                                }),
                'bio'        : forms.Textarea(attrs={
                                                'class': 'form-control'
                                                }),
                'location'   : forms.TextInput(attrs={
                                                'class': 'form-control'
                                                }),
                'birth_date' : forms.DateInput(attrs={
                                                'class': 'form-control',
                                                'placeholder': 'yyyy-mm-dd'
                                                }),
        }
        labels = {
                'avatar' : 'Change avatar'
        }     

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date and birth_date > datetime.date.today():
            raise ValidationError('Date of birth can not be in future')
        return birth_date

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            if len(avatar) > (2000 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 1 mb')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
