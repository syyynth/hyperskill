from django.urls import reverse
from django.views.generic import TemplateView, FormView

from .constants import FORM_PARTICIPANTS_NAME
from .models import FormRecord, FormData, FormField, FormModel


class HomePageView(TemplateView):
    template_name = 'forms/welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['participants'] = FormRecord.get_all_records()
        context['fields'] = FormField.get_fields_by_form_name(FORM_PARTICIPANTS_NAME)
        return context


class RegisterView(FormView):
    template_name = 'forms/register.html'

    @property
    def form_class(self):
        return FormModel.generate_dynamic_form_class(FORM_PARTICIPANTS_NAME)

    def form_valid(self, form):
        FormData.create_data(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')
