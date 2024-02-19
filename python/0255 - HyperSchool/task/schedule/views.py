from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, FormView

from .forms import EnrollForm, SearchForm
from .models import Course, Teacher


class MainView(ListView):
    model = Course
    template_name = 'schedule/main.html'
    context_object_name = 'courses'

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data['q']
            return Course.objects.filter(title__icontains=query)
        return Course.objects.all()


class CourseDetailView(DetailView):
    model = Course
    template_name = 'schedule/course_details.html'


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'schedule/teacher_details.html'


class EnrollView(FormView):
    form_class = EnrollForm
    template_name = 'schedule/enroll.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('enroll')


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'schedule/signup.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')
