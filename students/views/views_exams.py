# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Exam


# Views for Groups


def exams_list(request):
    exams = Exam.objects.all()

    # try to order exams list
    order_by = request.GET.get('order_by','')
    if order_by in ('date', 'subject', 'group'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()

    """# Paginate exams pages
    paginator = Paginator(exams, 3)
    page = request.GET.get('page')
    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        # If page is not integer, deliver first page
        exams = paginator.page(1)
    except EmptyPage:
        #if page is out of range (e.g. 9999), deliver last page result
        exams = paginator.page(paginator.num_pages)"""

    return render(request, 'students/exams_list.html', {'content': exams})

def exam_add(request):
    return HttpResponse('<h1>Exam Add Form</h1>')