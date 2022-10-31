from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

    # def clean_password1(self):
    #     password = self.cleaned_data.get('password1')
    #     if len(password) < 8:
    #         raise ValidationError("Password must be bigger than 8 Char")
    #     return password

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name', 'is_staff',
                  'is_active', 'is_admin')


# Login Logic
class UserLogin(forms.Form):
    query = forms.CharField(label='Username or email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        query_emailorusername = User.objects.filter(
            Q(username__iexact=query) |
            Q(email__iexact=query)
        ).distinct()
        # print(query_emailorusername)
        if not query_emailorusername.exists() and query_emailorusername.count() != 1:
            raise ValidationError('user is not exist')
        user_obj = query_emailorusername.first()
        # Please enter the correct email address and password
        if not user_obj.check_password(password):
            raise ValidationError('Password is Wrong')
        if not user_obj.is_active:
            raise ValidationError('User is not active')
        # print(user_obj)
        self.cleaned_data['user_obj'] = user_obj
        return super(UserLogin, self).clean(*args, **kwargs)
