# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.generic.base import TemplateView
from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div
from crispy_forms.bootstrap import FormActions

from datetime import datetime
from PIL import Image

from ..models import Student, Group
from ..util import paginate, get_current_group


class StudentsView(TemplateView):
    template_name = 'students/students_list.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(StudentsView, self).get_context_data(**kwargs)

        # check if we need to show only one group of students
        current_group = get_current_group(self.request)
        if current_group:
            object_list = Student.objects.filter(student_group=current_group)
        else:
            # otherwise show all students
            object_list = Student.objects.all()

        # try to order student list
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('id', 'last_name', 'first_name', 'ticket'):
            object_list = object_list.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                object_list = object_list.reverse()

        context = paginate(object_list, 5, self.request, context)

        return context


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
                    errors['birthday'] = \
                        u"Введіть коректний формат дати (напр. 1984-12-30)"
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
                        errors['photo'] = \
                            u"Виберіть зображення, що не перевищує 2 МБ"
                    else:
                        data['photo'] = photo
                except IOError:
                    errors['photo'] = u"Ви вибрали невірний тип файлу"
                except:
                    errors['photo'] = \
                        u"Виникла помилка при завантажені зображення!"

            # save student
            if not errors:
                # create student object
                student = Student(**data)
                # save it to database
                student.save()

                # redirect user to students list
                return HttpResponseRedirect(
                    u"""%s?success=1&amp;status_message=Студент
                    %s %s був успішно внесений до бази даних!"""
                    % (reverse('home'), data['last_name'], data['first_name']))

            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(
                u'%s?success=0&status_message=Додавання студента скасовано!'
                % reverse('home'))

    else:
        # initial form render
        return render(request, 'students/students_add.html',
                      {'groups': Group.objects.all().order_by('title')})


class StudentUpdateForm(ModelForm):

    class Meta:
        model = Student

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse(
            'students_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-5 control-label'
        self.helper.field_class = 'col-sm-7'

        # add buttons
        self.helper.layout[-1] = Div(
            Div(
                FormActions(
                    Submit(
                        'add_button', u'Зберегти',
                        css_class="btn btn-primary"),
                    Submit(
                        'cancel_button', u'Скасувати', css_class="btn-link"),
                ),
                #css_class="alert alert-info"
            ),
            #css_class="col-md-6 col-md-offset-3",
            css_id="form_button"
        )

class StudentUpdateView(UpdateView):

    """Class for editing students"""
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        return u'%s?success=1&status_message=Студента було успішно збережено!'\
            % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?success=0&status_message=Редагування студента відмінено!'
                % reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args,
                                                       **kwargs)


class StudentDeleteView(DeleteView):
    queryset = Student.objects.all()
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return u'%s?success=1&status_message=Студент був успішно видалений!'\
            % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?success=0&status_message=Видалення студента відмінено!'
                % reverse('home'))
        else:
            return super(StudentDeleteView, self).post(request,
                                                       *args, **kwargs)
