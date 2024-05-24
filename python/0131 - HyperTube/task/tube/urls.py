from django.urls import path

from tube.views import LoginView, LogoutView, MainView, SignUpView, UploadView, ViewView

urlpatterns = [
    path('tube/', MainView.as_view(), name='main'),
    path('tube/watch/<int:id>/', ViewView.as_view(), name='watch'),
    path('media/<path:path>/', ViewView.as_view(), name='serve'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('tube/upload/', UploadView.as_view(), name='upload'),
]
