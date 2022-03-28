from django import forms
from .models import CustomUser


class UserEditForm(forms.ModelForm): # 以下追記箇所
  picture = forms.FileField(label='picture', required=False)
  username = forms.CharField(label='user name')
  email = forms.EmailField(label='email')
  description = forms.CharField(label='自己紹介', widget=forms.Textarea) 

  class Meta:
    model = CustomUser
    fields = ('picture', 'username', 'email', 'description')
