from django.shortcuts import render
from . import core
from .forms import UserForm


def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data.get("address")
            radius = form.cleaned_data.get("radius")
            args = dict()
            args['form'] = form
            result = (core.Mapper(address).
                      create_map(cities=core.CsvReader.read_file(
                'D:\Программирование\Мои программы\кейс на стажера Fogstream\geoservice\geoservice\showmap\city.csv'),
                                 radius=core.Transform.euclidean_distance(radius)))
            if isinstance(result, str):
                args['resp'] = result
            else:
                args['resp'] = result._repr_html_()
    else:
        args = dict()
        form = UserForm()
        args['form'] = form
    return render(request, 'showmap/index.html', args)
