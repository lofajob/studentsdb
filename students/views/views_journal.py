# -*- coding: utf-8 -*-

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from ..models import Student, MonthJournal
from ..util import paginate


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)
        date_format = "%Y-%m-%d"

        # check if we need to display some specific month
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], date_format
                                      ).date()
        else:
            # otherwise just displaying current month data
            today = datetime.today()
            month = date(today.year, today.month, 1)

        # calculate current, previous and next month details;
        # we need this for month navigation element in template
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime(date_format)
        context['next_month'] = next_month.strftime(date_format)
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')

        # we'll use this variable in students pagination
        context['cur_month'] = month.strftime(date_format)

        # prepare variable for template to generate
        # journal table header elements
        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{'day': d,
                                    'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
                                   for d in range(1, number_of_days + 1)]

        # url to update studentpresence, for AJAX form post
        update_url = reverse('journal')

        # get all students from database and oreder them
        queryset = Student.objects.all().order_by('last_name')

        # go over all students and collect data about presence
        # during selected month
        students = []
        for student in queryset:
            # try to get journal object by month selected
            # month and current student
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None

            # fill in days presence list for current student
            days = []
            for day in range(1, number_of_days + 1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day%d' %
                                                   day, False) or False,
                    'date': date(myear, mmonth, day).strftime(
                        date_format),
                })

            # prepare metadata for current student
            students.append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        # apply pagination, 10 students per page
        context = paginate(students, 10, self.request, context,
                           var_name='students')

        # finally return updated context
        # with paginated students
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        # prepare student, dates and presence data
        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False
        student = Student.objects.get(pk=data['pk'])

        # get or create journal object for given student and month
        journal = MonthJournal.objects.get_or_create(student=student,
                                                     date=month)[0]

        # set new presence on journal for given student and save result
        setattr(journal, 'present_day%d' % current_date.day, present)
        journal.save()

        # return succes status
        return JsonResponse({'status': 'success'})
