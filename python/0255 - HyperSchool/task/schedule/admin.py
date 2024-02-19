from django.contrib import admin

from .models import Course, Student, Teacher

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Teacher)
