# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from datetime import datetime
from PIL import Image

from ..models import Student, Group


# Views for Students


def students_list(request):
    students = Student.objects.all()

    # try to order student list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # Paginate students' pages
    paginator = Paginator(students, 4)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not integer, deliver first page
        students = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page result
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', {'content': students})


def students_add(request):
    # was form posted?
    if request.method == 'POST':
        # was form add button clicked?
        if request.POST.get('add_button') is not None:

            # errors collection
            errors = {}

            # validate student data will go here
            data = {}
            data.update(csrf(request))

            # values middle_name and notes can be blank and so far not require
            # validation
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім’я є обов’язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов’язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов’язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors[
                        'birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов’язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(id=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Введіть коректну групу"
                else:
                    data['student_group'] = groups[0]
                #data['student_group'] = Group.objects.get(id=student_group)

            photo = request.FILES.get('photo')
            # validate photo
            if photo:
                try:
                    img = Image.open(request.FILES.get('photo'))
                    img.verify()

                    if photo.size > 2000000:
                        errors[
                            'photo'] = u"Виберіть зображення, що не перевищує 2 МБ"
                    else:
                        data['photo'] = photo
                except IOError:
                    errors['photo'] = u"Ви вибрали невірний тип файлу"
                except:
                    errors[
                        'photo'] = u"Виникла помилка при завантажені зображення!"

            # save student
            if not errors:
                # create student object
                student = Student(**data)
                # save it to database
                student.save()

                # redirect user to students list
                return HttpResponseRedirect(u'%s?success=1&amp;status_message=Студент %s %s був успішно внесений до бази даних!'
                                            % (reverse('home'), data['last_name'], data['first_name']))

            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(u'%s?success=0&status_message=Додавання студента скасовано!' % reverse('home'))

    else:
        # initial form render
        return render(request, 'students/students_add.html',
                      {'groups': Group.objects.all().order_by('title')})


def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s </h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s </h1>' % sid)
