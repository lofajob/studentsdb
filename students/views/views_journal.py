# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


# Views for Groups

def feed(request):
    return render(request, 'students/journal.html')