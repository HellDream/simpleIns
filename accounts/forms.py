from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'username',
                                                                               'id': 'username',
                                                                               'placeholder': 'Enter username'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'password',
                                                                                   'id': 'password',
                                                                                   'placeholder': 'Enter password'}))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean()

    @property
    def get_form(self):
        return "Login"


class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'username',
                                                             'id': 'username',
                                                             'placeholder': 'Enter username'}))
    email = forms.CharField(label='Email address', widget=forms.TextInput(attrs={'class': 'email',
                                                                                 'id': 'email',
                                                                                 'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password',
                                                                 'id': 'password',
                                                                 'placeholder': 'Enter password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password',
                                                                         'id': 'password',
                                                                         'placeholder': 'Confirm password'}))
    image = forms.ImageField(label='Image', widget=forms.FileInput(attrs={'id': 'file', 'style': 'display: none'}))

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm_password')
        if password != confirm:
            raise forms.ValidationError("Password does not match")
        email = User.objects.filter(email=self.cleaned_data.get('email'))
        if email.exists():
            raise forms.ValidationError("Email already existed")
        user = User.objects.filter(username=self.cleaned_data.get('username'))
        if user.exists():
            raise forms.ValidationError("username already existed")
        image = self.files.get('image')
        print image
        if not image:
            raise forms.ValidationError("Require your profile image.")
        return super(UserRegisterForm, self).clean()
    @property
    def get_form(self):
        return "registerForm"


class UserEditForm(forms.Form):
    signature = forms.CharField(label="Signature",
                                required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Signature'}))
    image = forms.ImageField(label="Image",
                             required=False,
                             widget=forms.FileInput(attrs={'id': 'file',
                                                           'style': 'display: none'}))

    @property
    def get_form(self):
        return "editForm"
