from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django_recaptcha.fields import ReCaptchaField

from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    slug = forms.CharField(max_length=128,
                           widget=forms.TextInput(
                               attrs={"class": "form-control mb-1"}))
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    bio = forms.CharField(max_length=512,
                          widget=forms.Textarea(attrs={'rows': 5, "class": "form-control mb-1"}))

    avatar = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control mb-1"}))

    class Meta:
        model = Profile
        fields = ('slug', 'birth_date', 'bio', 'avatar')


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=64,
                               widget=forms.TextInput(
                                   attrs={"class": "form-control mb-1"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    first_name = forms.CharField(max_length=64,
                                 widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    last_name = forms.CharField(max_length=64,
                                widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    recaptcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'recaptcha',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email



class UserRegisterForm(UserCreationForm):

    recaptcha = ReCaptchaField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'recaptcha',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Такой email уже используется в системе')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs.update({"placeholder": 'Ваш логин'})
            self.fields['email'].widget.attrs.update({"placeholder": 'Ваш E-mail'})
            self.fields['first_name'].widget.attrs.update({"placeholder": 'Ваше имя'})
            self.fields["last_name"].widget.attrs.update({"placeholder": 'Ваша фамилия'})
            self.fields['password1'].widget.attrs.update({"placeholder": 'Пароль'})
            self.fields['password2'].widget.attrs.update({"placeholder": 'Повторите пароль'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class UserLoginForm(AuthenticationForm):

    recaptcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'password', 'recaptcha',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'Логин'