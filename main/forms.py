from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Announcement, Note, Assignment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '0999-99-99-99'}))
    role = forms.ChoiceField(choices=User._meta.get_field('role').choices)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'role', 'password1', 'password2']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Announcement title'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write your announcement here...'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'download_url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Note title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the note'}),
            'download_url': forms.URLInput(attrs={'placeholder': 'https://example.com/note.pdf'}),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'download_url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Assignment title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the assignment'}),
            'download_url': forms.URLInput(attrs={'placeholder': 'https://example.com/assignment.pdf'}),
        }
