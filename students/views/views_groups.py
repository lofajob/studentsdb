# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from django.core.urlresolvers import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Div, Layout
from crispy_forms.bootstrap import FormActions

from ..models import Group, Student


# Views for Groups


def groups_list(request):
    groups = Group.objects.all()

    # try to order groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'title'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    # Paginate groups pages
    paginator = Paginator(groups, 4)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not integer, deliver first page
        groups = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page result
        groups = paginator.page(paginator.num_pages)

    return render(request, 'students/groups_list.html', {'content': groups})


class GroupForm(ModelForm):

    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_action = reverse('groups_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-5 control-label'
        self.helper.field_class = 'col-sm-7'

        # add buttons
        self.helper.layout = Layout(
            'title',
            'leader',
            'notes',
            Div(
                Div(
                    FormActions(
                        Submit(
                            'add_button', u'Зберегти', css_class="btn btn-primary"),
                        Submit(
                            'cancel_button', u'Скасувати', css_class="btn-link"),
                    ),
                    css_class="alert alert-info"
                ),
                css_class="col-md-6 col-md-offset-3",
                css_id="form_button"
            )
        )

class GroupFormUpd(GroupForm):

    def __init__(self, *args, **kwargs):
        super(GroupFormUpd, self).__init__(*args, **kwargs)

        self.helper.form_action = reverse(
            'groups_edit', kwargs={'pk': kwargs['instance'].id})


class GroupCreate(CreateView):
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('groups')

    def get_success_url(self):
        return u'%s?success=1&status_message=Група була успішно створена' % reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?success=0&status_message=Створення групи відмінено!' % reverse('groups'))
        else:
            return super(GroupCreate, self).post(request, *args, **kwargs)


class GroupEdit(UpdateView):
    model = Group
    form_class = GroupFormUpd
    success_url = reverse_lazy('groups')

    def get_success_url(self):
        return u'%s?success=1&status_message=Групу успішно відредаговано' % reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?success=0&status_message=Редагування групи відмінено!' % reverse('groups'))
        else:
            return super(GroupEdit, self).post(request, *args, **kwargs)


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        return u'%s?success=1&status_message=Група успішно видалена!' % reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?success=0&status_message=Видалення групи відмінено!' % reverse('groups'))
        else:
            return super(GroupDeleteView, self).post(request, *args, **kwargs)


def students_in_group(request, sid):
    students = Student.objects.all().filter(student_group=sid)
    group = Group.objects.get(id=sid)

    # try to order students list in group
    order_by = request.GET.get('order_by', '')
    if order_by == 'last_name':
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    return render(request, 'students/students_in_group.html', {'students': students, 'group': group})
