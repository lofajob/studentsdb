# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


# Views for Groups


def groups_list(request):
    groups = (
        {   'id': 1,
            'name': u'ЕК_31',
            'leader': {'id': 1, 'name': u"Павлюк Андрій"}},
        {   'id': 2,
            'name': u'ЕК_31',
            'leader': {'id': 2, 'name': u"Сорока Людмила"}},
        {   'id': 3,
            'name': u'ЕК_33',
            'leader': {'id': 3, 'name': u"Степан Бандера"}},
    )
    return render(request, 'students/groups_list.html', {'groups': groups})


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, sid):
    return HttpResponse('<h1>Edit Group %s </h1>' % sid)


def groups_delete(request, sid):
    return HttpResponse('<h1>Delete Group %s </h1>' % sid)