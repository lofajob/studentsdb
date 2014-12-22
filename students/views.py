# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


# Views for Students


def students_list(request):
	students = (
		{'id': 1,
		 'first_name': u'Павлюк',
		 'last_name': u'Андрій',
		 'ticket': u'2123',
		 'image': 'img/Dean.jpg'},
		{'id' : 2,
		 'first_name': u'Сорока',
		 'last_name': u'Людмила',
		 'ticket': u'2105',
		 'image': 'img/Female.jpg'},
		{'id' : 3,
		 'first_name': u'Степан',
		 'last_name': u'Бандера',
		 'ticket': u'1158',
		 'image': 'img/Stepa.jpg'},
	)

	return render(request, 'students/students_list.html', {'students': students })


def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s </h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s </h1>' % sid)


# Views for Groups


def groups_list(request):
    groups = (
        {   'id': 1,
            'name': u'ЕК_31',
            'lider_id': 2},
        {   'id': 2,
            'name': u'ЕК_31',
            'lider_id': 1},
        {   'id': 3,
            'name': u'ЕК_33',
            'lider_id': 3},
    )
    return render(request, 'groups/groups_list.html', {'groups': groups})


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, sid):
    return HttpResponse('<h1>Edit Group %s </h1>' % sid)


def groups_delete(request, sid):
    return HttpResponse('<h1>Delete Group %s </h1>' % sid)