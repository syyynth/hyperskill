from pathlib import Path

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView

from tube.forms import UploadForm
from tube.models import Tag, Video, VideoTag


class MainView(TemplateView):
    template_name = 'tube/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = self._get_videos()
        return context

    def _get_videos(self):
        q = self.request.GET.get('q')
        tag = self.request.GET.get('tag')

        videos = Video.objects.all()
        if q:
            videos = videos.filter(title__icontains=q)
        if tag:
            videos = videos.filter(videotag__tag__name__icontains=tag)

        return videos


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'tube/login.html'

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )
        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())
        return super().form_invalid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('main'))


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'tube/signup.html'
    success_url = reverse_lazy('login')


class UploadView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    form_class = UploadForm
    template_name = 'tube/upload.html'

    def form_valid(self, form):
        video = Video.objects.create(
            file=form.cleaned_data['video'],
            title=form.cleaned_data['title']
        )

        tags = form.cleaned_data['tags'].split()
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            VideoTag.objects.create(tag=tag, video=video)

        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('main'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main')


class ViewView(TemplateView):
    template_name = 'tube/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            video = Video.objects.get(id=kwargs['id'])
        except Video.DoesNotExist:
            raise Http404('Video not found')
        context['video'] = video
        context['tags'] = [tag.tag.name for tag in video.videotag_set.all()]
        return context

    def get(self, request, *args, **kwargs):
        if 'path' in kwargs:
            return self.serve_video(kwargs['path'])
        return super().get(request, *args, **kwargs)

    def serve_video(self, path):
        file_path = Path(settings.MEDIA_ROOT) / path

        if file_path.exists():
            response = FileResponse(open(file_path, 'rb'))
            response['Accept-Ranges'] = 'bytes'
            return response

        raise Http404('File not found')
