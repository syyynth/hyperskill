from django.urls import path

from .views import CourseDetailView, EnrollView, MainView, TeacherDetailView

urlpatterns = [
    path('main/', MainView.as_view(), name='main'),
    path('course_details/<int:pk>', CourseDetailView.as_view(), name='course_details'),
    path('teacher_details/<int:pk>', TeacherDetailView.as_view(), name='teacher_details'),
    path('add_course/', EnrollView.as_view(), name='enroll'),
]
