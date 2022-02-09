from django.http import HttpResponse


message = 'привет, здесь будет выводиться карта'


def index(request):
    return HttpResponse(message)
