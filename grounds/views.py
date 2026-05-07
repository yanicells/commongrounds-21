from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'grounds/post_list.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'grounds/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user.profile
            comment.save()
            return redirect('grounds:post-detail', pk=self.object.pk)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'grounds/post_form.html'
    success_url = reverse_lazy('grounds:post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'grounds/post_form.html'
    success_url = reverse_lazy('grounds:post-list')

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user.profile)
