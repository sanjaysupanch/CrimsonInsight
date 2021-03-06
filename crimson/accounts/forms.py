from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class AllauthSignupForm(forms.Form):
 
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
 
    def signup(self, request, user):
        """ Required, or else it throws deprecation warnings """
        pass


class releaseForm(forms.ModelForm):
		
    key = forms.CharField(label='Enter your Key',min_length=8, max_length=100, help_text='_')
    domain_name = forms.CharField(label='Enter your Domain name', max_length=100, help_text='Ex: www.google.com', )
    
    class Meta:
        model=releaseapk
        fields=('domain_name', 'key',)
	    
class documentForm(forms.ModelForm):
    class Meta:
        model= appname_and_image
        fields=('app_name', 'app_icon')
