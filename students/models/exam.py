# -*- coding: utf-8 -*-

from django.db import models


class Exam(models.Model):
    """Examination Model"""

    class Meta(object):
        verbose_name = u"Іспит"
        verbose_name_plural = u"Іспити"
        ordering = ["date"]

    date = models.DateTimeField(
        blank=False,
        verbose_name=u"Дата та час проведення")

    group = models.OneToOneField('Group',
        verbose_name=u"Група",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

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
        return u"%s, %s" % (self.subject, self.group.title)