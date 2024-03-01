from django.shortcuts import redirect
from django.views.generic import FormView, ListView, TemplateView

from record.forms import RegexForm
from record.models import Record
from record.services import RegexService

regex_service = RegexService()


class MainPageView(FormView):
    template_name = 'record/regex.html'
    form_class = RegexForm

    def form_valid(self, form):
        form.instance.result = regex_service.match(regex=form.cleaned_data['regex'],
                                                   text=form.cleaned_data['text'])
        form.save()
        return redirect('record', pk=form.instance.pk)


class RecordView(TemplateView):
    template_name = 'record/response.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record'] = Record.objects.get(pk=kwargs.get('pk'))
        return context


class RecordListView(ListView):
    model = Record
    template_name = 'record/history.html'
    context_object_name = 'records'

    def get_queryset(self):
        return Record.objects.all().order_by('-pk')
