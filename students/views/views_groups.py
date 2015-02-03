# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Group, Student


# Views for Groups


def groups_list(request):
    groups = Group.objects.all()

    # try to order groups list
    order_by = request.GET.get('order_by','')
    if order_by in ('id', 'title'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()
    elif not order_by:
        groups = groups.order_by('title')

    # Paginate groups pages
    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not integer, deliver first page
        groups = paginator.page(1)
    except EmptyPage:
        #if page is out of range (e.g. 9999), deliver last page result
        groups = paginator.page(paginator.num_pages)

    return render(request, 'students/groups_list.html', {'content': groups})


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, sid):
    return HttpResponse('<h1>Edit Group %s </h1>' % sid)


def groups_delete(request, sid):
    return HttpResponse('<h1>Delete Group %s </h1>' % sid)


def students_in_group(request, sid):
    students = Student.objects.all().filter(student_group=sid)
    group = Group.objects.get(id=sid)

    # try to order students list in group
    order_by = request.GET.get('order_by','')
    if order_by in ('id', 'last_name'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    return render(request, 'students/students_in_group.html', {'students': students, 'group': group})