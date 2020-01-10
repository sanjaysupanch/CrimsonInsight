from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

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


class debugForm(forms.ModelForm):
		
	# key = forms.CharField(label='Enter your key', max_length=100 )
	class Meta:
		model = debugapk
		fields=('domain_name',)


class releaseForm(forms.ModelForm):
		
    key = forms.CharField(label='Enter your key', max_length=100)
    
    class Meta:
        model=releaseapk
        fields=('domain_name', 'key',)
	    

