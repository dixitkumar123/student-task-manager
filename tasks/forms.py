from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task

# Custom SignUp Form - Built-in UserCreationForm ko extend kar rahe hain taaki CSS classes add kar sakein
class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Student Email ID'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # HTML inputs par CSS class aur placeholder apply kar rahe hain
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose Username'
        })
        self.fields['username'].help_text = ''
        
        # Password fields styling
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Enter Password'
            })
            self.fields['password1'].help_text = ''
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            })
            self.fields['password2'].help_text = ''


# Task Form - Student task add aur edit karne ke liye ModelForm
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # Sirf wahi fields jo student fill karega (user background mein link hoga)
        fields = ['title', 'description', 'priority', 'due_date', 'status']

        # Widgets customization for smooth UI inputs
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Task Title (e.g. Complete Django Assignment)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add details, notes or links for this task...'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control select-control'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # HTML5 Date Picker UI
            }),
            'status': forms.Select(attrs={
                'class': 'form-control select-control'
            }),
        }
