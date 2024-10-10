from django import forms
from .models import Route

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'cities', 'description', 'estado']  # Campos que se mostrarán en el formulario
        widgets = {
            'cities': forms.Textarea(attrs={'rows': 3}),  # Para que el campo de cities sea un textarea
            'description': forms.Textarea(attrs={'rows': 3}),
        }