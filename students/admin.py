from django.contrib import admin
from .models import Student, Group, Exam, Exam_result

# Register your models here.
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Exam)
admin.site.register(Exam_result)
