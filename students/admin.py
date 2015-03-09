# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

from .models.student import Student
from .models.group import Group
from .models.exam import Exam, Exam_result


# Method for copy action
def copy_items(modeladmin, request, queryset):
    for object in queryset:
        # this way lets us to copy element
        object.pk = None
        object.save()
copy_items.short_description = u"Копіювати обрані елементи"


class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        """
        Check if student is leader in any group.

        If yes, then ensure it's the same as selected group.
        """

        # get a group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and \
                self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи.',
                                  code='invalid')

        return self.cleaned_data['student_group']


class GroupFormAdmin(ModelForm):

    def clean_leader(self):
        """
        If a student is in another group, then he can't be installed
        """
        # Set warning message
        error_message = u'Студент %s не може бути старостою. Він належить до іншої групи'

        students = Student.objects.filter(student_group=self.instance)

        if self.cleaned_data['leader'] is None:
            # Set empty value in leader attribute
            setattr(self.instance, 'leader', self.cleaned_data['leader'])
        elif self.cleaned_data['leader'] not in students:
            raise ValidationError(error_message % (self.cleaned_data['leader']),
                                  code='invalid')

        return self.cleaned_data['leader']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['ticket']
    ordering = ['last_name']
    list_per_page = 10
    search_fields = [
        'last_name', 'first_name', 'middle_name', 'ticket', 'notes']
    actions_on_top = False
    actions_on_bottom = True
    actions = [copy_items]
    form = StudentFormAdmin

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader', 'notes']
    list_display_links = ['title']
    ordering = ['title']
    list_per_page = 10
    search_fields = ['title', 'notes']
    actions_on_top = False
    actions_on_bottom = True
    form = GroupFormAdmin


# Register models
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)
admin.site.register(Exam_result)
