from django.forms import TextInput, Form, CharField


class UserForm(Form):
    address = CharField(max_length=100)
    radius = CharField(max_length=10, required=False)
    widgets = {
        "address": TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите адрес"
        }),
        "radius": TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите радиус"
        }),
    }
