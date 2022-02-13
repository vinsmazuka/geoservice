from django.shortcuts import render

from . import core
from .forms import UserForm
from .models import City


def index(request):
    row_data = list(City.objects.all())
    cities = {city.city: {'geo_lat': city.geo_lat,
                          'geo_lon': city.geo_lon} for city in row_data}
    args = dict()
    if request.method == 'POST':
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
    else:
        form = UserForm()
        args['form'] = form
    return render(request, 'showmap/index.html', args)
