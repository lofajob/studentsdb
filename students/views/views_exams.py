# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Exam, Exam_result


# Views for Groups


def exams_list(request):
    exams = Exam.objects.all()

    # try to order exams list
    order_by = request.GET.get('order_by','')
    if order_by in ('date', 'subject', 'group_examing'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()

    return render(request, 'students/exams_list.html', {'content': exams})


def exam_result(request, sid):
    results = Exam_result.objects.all().filter(exam_res=sid)
    exam = Exam.objects.get(id=sid)

    # try to order students list in group
    order_by = request.GET.get('order_by','')
    if order_by == 'last_name':
        results = results.order_by('student_res')
        if request.GET.get('reverse', '') == '1':
            results = results.reverse()

    return render(request, 'students/exam_result.html', {'results': results, 'exam': exam})


def exam_add(request):
    return HttpResponse('<h1>Exam Add Form</h1>')