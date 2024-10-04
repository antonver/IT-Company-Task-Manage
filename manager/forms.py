from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from manager.models import Task, Worker, Project, TaskType, Position


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                                             'class': 'datepicker'}))

    class Meta:
        model = Task
        fields = "__all__"



class TaskFilterForm(forms.Form):
    is_completed = forms.BooleanField(required=False, label="Is completed?")
    priority = forms.ChoiceField(choices=Task.PRIORITY_CHOICES, required=False, label="Priority")
    project = forms.ModelChoiceField(required=False, queryset=Project.objects.all(), label="Project",
                                     empty_label="All Projects")
    task_type = forms.ModelChoiceField(required=False, queryset=TaskType.objects.all(), label="Task Type",
                                       empty_label="Any Task Type")
    assignees = forms.ModelChoiceField(required=False, queryset=get_user_model().objects.all(), label="Assignees",
                                       empty_label="assignees")

    def clean_priority(self):
        priority = self.cleaned_data.get("priority")
        if priority == '':
            return None  # Handle empty string by returning None
        return priority


class TaskSearchForm(forms.Form):
    name = forms.CharField(required=True, max_length=255)


class RegistrationForm(UserCreationForm):
    model = Worker
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            "position": forms.ModelChoiceField(attrs={
                "class": "form-control",
                "placeholder": "Position"
            }, queryset=get_user_model().objects.select_related(Position), label="Position"
            )
        }


class LoginForm(AuthenticationForm):
    model = Worker
    username = UsernameField(label=_("Your Username"),
                             widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
    password = forms.CharField(
        label=_("Your Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )


class UserPasswordResetForm(PasswordResetForm):
    model = Worker
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))


class UserSetPasswordForm(SetPasswordForm):
    model = Worker
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")


class UserPasswordChangeForm(PasswordChangeForm):
    model = Worker
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Old Password'
    }), label='Old Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")