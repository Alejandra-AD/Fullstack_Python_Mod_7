
from django import forms
from .models import Etiqueta, Task


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
    etiquetas = forms.ModelMultipleChoiceField(queryset=Etiqueta.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)


class TaskForm(forms.ModelForm):
    etiquetas = forms.ModelMultipleChoiceField(queryset=Etiqueta.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'etiquetas']