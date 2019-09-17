from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class HoodForm(forms.ModelForm):
    class Meta:
        model = Neighbourhood
        exclude = ['admin','content']

class EditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','photo']
class NewReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['neighbourhood','judge']

class BusinessForm(forms.ModelForm):
    class Meta:
            model = Business
            exclude = ['neighbourhood', 'profile']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'neighbourhood']

class NewCommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    exclude = ['post','postername','pub_date']