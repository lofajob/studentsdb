from django.http import HttpRequest

#from .settings import PORTAL_URL


def students_proc(request):
    return {'PORTAL_URL': 'http://' + request.META['SERVER_NAME'] + ':' + request.META['SERVER_PORT']}
