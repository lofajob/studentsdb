from django.conf.urls import patterns, include, url
from django.contrib import admin
#from students.views.contact_admin import Contact_admin
from students.views.views_students import StudentsView, StudentUpdateView, \
                                          StudentDeleteView
from students.views.views_groups import GroupsView, GroupCreate, \
                                        GroupEdit, GroupDeleteView
from students.views.views_journal import JournalView


from .settings import MEDIA_ROOT, DEBUG

urlpatterns = patterns('',
           # Examples:
           # url(r'^$', 'studentdb.views.home', name='home'),
           # url(r'^blog/', include('blog.urls')),

           # Students urls
           url(r'^$', StudentsView.as_view(),
               name='home'),
           url(r'^students/add/$',
            'students.views.views_students.students_add', name='students_add'),
           url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(),
               name='students_edit'),
           url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(),
               name='students_delete'),

           # Groups urls
           url(r'^groups/$', GroupsView.as_view(),
               name='groups'),
           url(r'^groups/add/$', GroupCreate.as_view(),
               name='groups_add'),
           url(r'^groups/(?P<pk>\d+)/edit/$',
               GroupEdit.as_view(), name='groups_edit'),
           url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(),
               name='groups_delete'),
           url(r'^groups/(?P<sid>\d+)/students_in_group/$',
               'students.views.views_groups.students_in_group',
               name='students_in_group'),

           # Journal urls
           url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(),
               name='journal'),



           # Exams urls
           url(r'^exams/$',
               'students.views.views_exams.exams_list', name='exams'),
           url(r'^exams_add/$', 'students.views.views_exams.exam_add',
               name='exam_add'),
           url(r'^exams/(?P<sid>\d+)/exam_result/$',
               'students.views.views_exams.exam_result', name='exam_result'),

           # Admin urls
           url(r'^admin/', include(admin.site.urls)),

           # Contact Admin
           url(r'^contact-admin/$',
               'students.views.contact_admin.contact_admin',
               name='contact_admin'),
           )

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$',
                                'django.views.static.serve', {
                                    'document_root': MEDIA_ROOT}))
