# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Group


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

    # Paginate students' pages
    """paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not integer, deliver first page
        students = paginator.page(1)
    except EmptyPage:
        #if page is out of range (e.g. 9999), deliver last page result
        students = paginator.page(paginator.num_pages)"""

    return render(request, 'students/groups_list.html', {'groups': groups})


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, sid):
    return HttpResponse('<h1>Edit Group %s </h1>' % sid)


def groups_delete(request, sid):
    return HttpResponse('<h1>Delete Group %s </h1>' % sid)