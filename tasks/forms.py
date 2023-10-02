from django import forms
from .models import Task

class Task_form(forms.ModelForm):
  class Meta:
    model = Task
    fields = ['title', 'description', 'important']
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form--title', 'placeholder': 'Write a title'}),
      'description': forms.Textarea(attrs={'class': 'form--description', 'placeholder': 'Write a description'}),
      'important': forms.CheckboxInput(attrs={'class': 'form--important'}),
    }