from django.shortcuts import render

from . import core
from .forms import UserForm
from .models import City

row_data = list(City.objects.all())


def index(request):
    cities = {city.city: {'geo_lat': city.geo_lat,
                          'geo_lon': city.geo_lon} for city in row_data}
    args = dict()

    def post_response():
        """формирует ответ в случае поступления POST-запроса"""
        form = UserForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data.get("address")
            radius = form.cleaned_data.get("radius")
            args['form'] = form
            result = (core.Mapper(address).
                      create_map(cities=cities,
                                 radius=core.transform_radius(radius)))
            if isinstance(result, str):
                args['resp'] = result
            else:
                args['resp'] = result._repr_html_()

    def get_response():
        """формирует ответ в случае поступления GET-запроса"""
        form = UserForm()
        args['form'] = form

    possible_responses = {
        'POST': post_response,
        'GET': get_response
    }
    possible_responses[request.method]()
    return render(request, 'showmap/index.html', args)
