from django import forms
from django.core.exceptions import ValidationError

from .models import Tag, Post

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
#        if Tag.objects.filter(slug__iexact=new_slug).count():
#            raise ValidationError(
#                'Slug must be unique. We have "{}" slug already'.format(new_slug)
#                )
        return new_slug

#    def clean_title(self):
#        new_title = self.cleaned_data['title']
#
#        if Tag.objects.filter(title__iexact=new_title).count():
#            raise ValidationError(
#                'Tag must be unique. We have "{}" tag already'.format(new_title)
#                )
#        return new_title


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
