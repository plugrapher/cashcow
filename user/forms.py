from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Post,Tag
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

class PostForm(ModelForm):
	class Meta:
		model = Post
		#fields = '__all__'
		fields = [ 'jobtitle', 'sub_title', 'location' , 'salary' , 'qualification']

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']
		

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'first_name', 'last_name','balance']



class QRCodeForm(forms.Form):
        text_data = forms.CharField(label='Text to Encode', max_length=255)
