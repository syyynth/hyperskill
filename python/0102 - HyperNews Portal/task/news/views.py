from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from hypernews.settings import NEWS_JSON_PATH
from news.forms import ArticleForm
from news.services import NewsService

news_service = NewsService(NEWS_JSON_PATH)


class MainPageView(TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        context['news'] = news_service.get_news(q)
        return context


class ArticleView(TemplateView):
    template_name = 'news/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = news_service.get_single(context['n'])
        return context


class PostView(FormView):
    template_name = 'news/post.html'
    form_class = ArticleForm

    def form_valid(self, form):
        news_service.add(title=form.cleaned_data.get('title'),
                         text=form.cleaned_data.get('text'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')
