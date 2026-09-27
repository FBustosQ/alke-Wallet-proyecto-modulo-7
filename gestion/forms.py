from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente

        fields = [
            "nombre",
            "email",
            "telefono",
        ]

        label = {
            "nombre": "Nombre completo",
            "email": "Correo electrónico",
            "telefono": "Teléfono"
        }

        widgets = {
            "nombre" : forms.TextInput(attrs={ "class":"form-control"}),
            "email" : forms.EmailInput(attrs={"class":"form-control"}),
            "telefono" : forms.TextInput(attrs={"class":"form-control"}),
        }