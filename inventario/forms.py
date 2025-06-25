from django import forms
from .models import Producto

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