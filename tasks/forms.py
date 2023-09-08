from django.forms import ModelForm
from .models import Task

class Task_form(ModelForm):
  class Meta:
    model = Task
    fields = ['title', 'description', 'important']