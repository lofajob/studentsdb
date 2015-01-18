# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Student


# Views for Students


def students_list(request):
	students = Student.objects.all()

	# try to order student list
	order_by = request.GET.get('order_by','')
	if order_by in ('id', 'last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
	else:
		students = students.order_by('last_name')

	# Paginate students' pages
	paginator = Paginator(students, 4)
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		# If page is not integer, deliver first page
		students = paginator.page(1)
	except EmptyPage:
		#if page is out of range (e.g. 9999), deliver last page result
		students = paginator.page(paginator.num_pages)

	return render(request, 'students/students_list.html', {'content': students })


def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s </h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s </h1>' % sid)
