from django.shortcuts import render
from . import core


def index(request):
    args = dict()
    result = (core.Mapper('Киров').
        create_map(cities=core.CsvReader.read_file('D:\Программирование\Мои программы\кейс на стажера Fogstream\geoservice\geoservice\showmap\city.csv'),
                   radius=core.Transform.euclidean_distance('400')))
    if isinstance(result, str):
        args['resp'] = result
    else:
        args['resp'] = result._repr_html_()
    return render(request, 'showmap/index.html', args)
