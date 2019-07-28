from django.http import HttpResponse


def myfirstview(request):
    return HttpResponse('hello')