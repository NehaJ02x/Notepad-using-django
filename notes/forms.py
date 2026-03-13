from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Note, Category, Tag


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NoteForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Comma-separated tags'}),
        help_text='Enter tags separated by commas',
    )

    class Meta:
        model = Note
        fields = ['title', 'body', 'category', 'color', 'is_pinned', 'reminder']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Note title'}),
            'body': forms.Textarea(attrs={'id': 'note-body'}),
            'color': forms.Select(),
            'reminder': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
        if self.instance.pk:
            self.fields['tags_input'].initial = ', '.join(
                t.name for t in self.instance.tags.all()
            )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
