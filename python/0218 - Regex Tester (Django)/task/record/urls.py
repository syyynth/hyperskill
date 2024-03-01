from django.urls import path

from record.views import MainPageView, RecordListView, RecordView

urlpatterns = [
    path('history/', RecordListView.as_view(), name='history'),
    path('', MainPageView.as_view(), name='main'),
    path('result/<int:pk>/', RecordView.as_view(), name='record'),
]
