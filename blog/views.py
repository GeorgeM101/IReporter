from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, HttpResponse, redirect
from .forms import Video_form
from .models import Video
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)


# def base(request):
#     return render(request, 'blog/base.html')

def about(request):
    return render(request, 'blog/about.html', {'title': "About Page"})


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Video upload section


def video(request):
    form = Video_form()
    all_video = Video.objects.all()
    if request.method == "POST":
        form = Video_form(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse("<h1> Uploaded successfully </h1>")
    else:
        form = Video_form()
    return render(request, 'blog/videos.html', {"form": form, "all": all_video})


def success(request):
    return render(request, 'success.html')


def contact(request):

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)
        return render(request, 'blog/success.html', {'email': email})

    return render(request, 'blog/contact.html', {})
