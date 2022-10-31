from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# 'username', 'first_name', 'last_name', 'email', 'password1', 'password2'
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # to add any class to input fields
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


# password1 = forms.CharField(widget=forms.PasswordInput(attrs={
#     'class': 'form-control',
#     'placeholder': 'Enter Password'
# }))

# def __init__(self, *args, **kwargs):
#     super(RegisterForm, self).__init__(*args, **kwargs)
#     self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
#     for field in self.fields:
#         self.fields[field].widget.attrs['class'] = 'form-control'
