from django.forms import Form, CharField


class UserForm(Form):
    """
    Класс, предназначенный
    для ввода данных пользователем
    """
    address = CharField(max_length=100)
    radius = CharField(max_length=10, required=False)
    address.widget.attrs.update(size='100')
    address.widget.attrs.update(placeholder="Введите адрес, "
                                            "к примеру: Москва, "
                                            "или: Хабаровск, Муравьева-Амурского 33(только РФ)")
    radius.widget.attrs.update(size='15')
    radius.widget.attrs.update(placeholder='Введите радиус')
