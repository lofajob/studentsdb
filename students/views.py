from django.shortcuts import render
from django.http import HttpResponse


# Views for Students


def students_list(request):
    return render(request, 'students/students_list.html', {})


def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s </h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s </h1>' % sid)


# Views for Groups


def groups_list(request):
    return HttpResponse('<h1>Groups Listing</h1>')


def groups_add(request):
    return HttpResponse('<h1Group Add Form</h1>')


def groups_edit(request, sid):
    return HttpResponse('<h1>Edit Group %s </h1>' % sid)


def groups_delete(request, sid):
    return HttpResponse('<h1>Delete Group %s </h1>' % sid)