from django import forms
from .models import Producto
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

def clean(self):
        cleaned_data = super().clean()
        stock = cleaned_data.get('stock')
        nivel_minimo = cleaned_data.get('nivel_minimo')

        if stock is not None and nivel_minimo is not None:
            if stock < nivel_minimo:
                raise forms.ValidationError(
                    "El stock no puede ser menor que el nivel mínimo."
                )
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'input'}))

class UserRegistroForm(forms.ModelForm):

    is_staff = forms.BooleanField(label="¿Es administrador?", required=False)

    password1 = forms.CharField( widget=forms.PasswordInput(attrs={'class': 'input'}), label='Contraseña')
    password2 = forms.CharField( widget=forms.PasswordInput(attrs={'class': 'input'}), label='Confirmar Contraseña')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'is_staff']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'email': 'Correo Electrónico',
            'is_staff': '¿Es administrador?',
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "input"}),
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cd['password2']

class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), label='Nueva Contraseña', required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), label='Confirmar Nueva Contraseña', required=False)

    class Meta:
        model = User
        fields = ['username']
        labels = {
            "username": "Nombre de usuario",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "input"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

class UserUpdateForm(forms.ModelForm):
    password_actual = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input'}),
        label='Contraseña actual',
        required=True
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input'}),
        label='Nueva Contraseña',
        required=False
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input'}),
        label='Confirmar Nueva Contraseña',
        required=False
    )

    class Meta:
        model = User
        fields = ['username']
        labels = {
            "username": "Nombre de usuario",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "input"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        password_actual = cleaned_data.get("password_actual")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not self.user.check_password(password_actual):
            raise forms.ValidationError("La contraseña actual es incorrecta.")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Las nuevas contraseñas no coinciden.")

        return cleaned_data
