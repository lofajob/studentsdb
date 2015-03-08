# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

from .models import Student, Group, Exam, Exam_result


class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        """Check if student is leader in any group.

        If yes, then ensure it's the same as selected group.  """

        # get group where current studentd is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and \
                self.cleaned_data['student_group'] not in groups:
            raise ValidationError(
                u'Студент є старостою іншої групи.', code='invalid')

        return self.cleaned_data['student_group']


class GroupFormAdmin(ModelForm):

    def clean_leader(self):
        students = Student.objects.filter(student_group=self.instance)
        if len(students) > 0 and \
                self.cleaned_data['leader'] not in students admin \
                self.cleaned_data['leader'] is not None:
            raise ValidationError(
                u'Староста повинен бути студентом групи', code='invalid')

        return self.cleaned_data['leader']


# Method for copy action
def copy_items(modeladmin, request, queryset):
    for object in queryset:
        # this way lets us to copy element
        object.pk = None
        object.save()
copy_items.short_description = u"Копіювати обрані елементи"


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
