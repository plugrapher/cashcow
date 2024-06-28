from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Post,Transaction,Wallet
from django.forms import ModelForm

#import qrcode


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',  'email', 'phone_no', 'password1', 'password2']

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Post'))


class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']
		

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
       # fields = ['username', 'email', 'first_name', 'last_name','balance']
        fields = '__all__'



class QRCodeForm(forms.Form):
        text_data = forms.CharField(label='Text to Encode', max_length=255)


class BitcoinTopUpForm(forms.Form):
    class Meta:

        bitcoin_amount = forms.DecimalField(label='Bitcoin Amount', min_value=0)
