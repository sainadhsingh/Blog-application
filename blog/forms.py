from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Profile, Post, Comment, Category, Tag

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    bio = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself...'}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['bio', 'avatar', 'email', 'first_name', 'last_name']:
                field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            if self.cleaned_data.get('bio'):
                profile.bio = self.cleaned_data['bio']
            if self.cleaned_data.get('avatar'):
                profile.avatar = self.cleaned_data['avatar']
            profile.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'location', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        help_text="Comma-separated tags (e.g. Python, WebDev, Django)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, WebDev, Django'})
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'featured_image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a descriptive post title'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'content': CKEditor5Widget(config_name='extends', attrs={'class': 'django_ckeditor_5'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags_input'].initial = ", ".join(t.name for t in self.instance.tags.all())

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            self._save_tags(post)
        return post

    def _save_tags(self, post):
        tags_str = self.cleaned_data.get('tags_input', '')
        tag_objs = []
        if tags_str:
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            for name in tag_names:
                tag = Tag.objects.filter(name__iexact=name).first()
                if not tag:
                    tag = Tag.objects.create(name=name)
                tag_objs.append(tag)
        post.tags.set(tag_objs)


class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your thoughts...'
            })
        }
