from django.forms import ModelForm
from .models import Todo

class TodoForms(ModelForm):
    class Meta: # initailize the sub class that we need
        model = Todo
        fields = ['title', 'memo', 'important']
