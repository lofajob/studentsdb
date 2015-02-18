# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime


class Exam(models.Model):

    """Examination Model"""

    class Meta(object):
        verbose_name = u"Іспит"
        verbose_name_plural = u"Іспити"
        ordering = ["date"]

    date = models.DateTimeField(
        blank=False,
        verbose_name=u"Дата та час проведення")

    group_examing = models.ForeignKey('Group',
        blank=False,
        null=True,
        verbose_name=u"Група")

    subject = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Предмет")

    educator = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Викладач")

    place = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Аудиторія")

    def __unicode__(self):
        return u"%s, %s" % (self.subject, self.group_examing.title)


class Exam_result(models.Model):

    """Model for result of examination"""

    class Meta(object):
        verbose_name = u"Результати іспиту"
        verbose_name_plural = u"Результати іспиту"
        #ordering = ["student_res"]

    exam_res = models.ForeignKey('Exam', verbose_name=u"Іспит")

    student_res = models.ForeignKey('Student', verbose_name=u"Студент")
    #, limit_choices_to={'student_group_id': Exam.group}

    grade = models.IntegerField(
        max_length=3,
        blank=True,
        null=True,
        verbose_name=u"Результат")

    def __unicode__(self):
        return u"%s %s" % (self.student_res.last_name, self.student_res.first_name)
