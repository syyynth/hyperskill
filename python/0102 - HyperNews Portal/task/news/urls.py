from django.urls import path
from django.views.generic import RedirectView

from news.views import ArticleView, MainPageView, PostView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='main')),

    path('news/', MainPageView.as_view(), name='main'),
    path('news/<int:n>/', ArticleView.as_view(), name='article'),
    path('news/create/', PostView.as_view(), name='create')
]
