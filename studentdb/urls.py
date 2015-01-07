from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studentdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Students urls
    url(r'^$', 'students.views.views_students.students_list', name='home'),
    url(r'^students/<add></add>/$', 'students.views.views_students.students_add', name='students_add'),
    url(r'^students/(?P<sid>\d+)/edit/$', 'students.views.views_students.students_edit', name='students_edit'),
    url(r'^students/(?P<sid>\d+)/delete/$', 'students.views.views_students.students_delete', name='students_delete'),

    # Groups urls
    url(r'^groups/$', 'students.views.views_groups.groups_list', name='groups'),
    url(r'^groups/add/$', 'students.views.views_groups.groups_add', name='groups_add'),
    url(r'^groups/(?P<sid>\d+)/edit/$', 'students.views.views_groups.groups_edit', name='groups_edit'),
    url(r'^groups/(?P<sid>\d+)/delete/$', 'students.views.views_groups.groups_delete', name='groups_delete'),

    # Journal urls
    url(r'^journal/', 'students.views.views_journal.feed', name='journal'),

    # Admin urls
    url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    #serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT}))
