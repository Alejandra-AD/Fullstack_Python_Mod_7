
from django import forms
from .models import Etiqueta,Task,Priority,User


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', required=True,
                                max_length=50, min_length=5,
                                error_messages={
                                    'required': 'El usuario es obligatorio',
                                    'max_length': 'El usuario no puede superar los 50 caracteres',
                                    'min_length': 'El usuario debe tener al menos 5 caracteres'
                                },
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Ingrese su usuario',
                                    'class': 'form-control'
                                })
                                )
    password = forms.CharField(label='Contraseña', required=True,
                                max_length=50, min_length=1,
                                error_messages={
                                    'required': 'La contraseña es obligatoria',
                                    'max_length': 'La contraseña no puede superar los 50 caracteres',
                                    'min_length': 'La contraseña debe tener al menos 1 caracter'
                                },
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Ingrese su contraseña',
                                    'class': 'form-control'
                                })
                                )


class TaskFilterForm(forms.Form):
    name = forms.CharField(required=False)
    due_date = forms.DateField(required=False)
    etiqueta = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), required=False, widget=forms.Select)
    priority = forms.ModelChoiceField(queryset=Priority.objects.all(), required=False, widget=forms.Select)
    
class TaskForm(forms.ModelForm):
    etiqueta = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), empty_label=None)
    priority = forms.ModelChoiceField(queryset=Priority.objects.all(), empty_label=None)
    user = forms.ModelChoiceField(queryset=User.objects.all(), label='Usuario')

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'etiqueta', 'priority', 'user']
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['title'].widget.attrs['placeholder'] = 'Ingrese el título de la tarea'
            self.fields['description'].widget.attrs['placeholder'] = 'Ingrese la descripción de la tarea'
