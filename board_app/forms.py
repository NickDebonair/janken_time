from django import forms
from .models import Topics, Texts

class CreateTopicForm(forms.ModelForm):
  title = forms.CharField(label='Title')

  class Meta:
    model = Topics
    fields = ('title',)


class DeleteTopicForm(forms.ModelForm): # 以下追記箇所

  class Meta:
    model = Topics
    fields = []


class PostTextForm(forms.ModelForm): # 追記箇所
  text = forms.CharField(
    label='', 
    widget=forms.Textarea(attrs={
      'rows':10,
      'cols':50
      })
    )
    
  class Meta:
    model = Texts
    fields = ('text',)
