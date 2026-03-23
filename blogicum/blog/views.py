from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (ListView, DetailView, CreateView, DeleteView,
                                  UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Count

from .forms import CommentForm
from .models import Post, Category, Comment


User = get_user_model()


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_queryset(self):
        self.profile = get_object_or_404(
            User,
            username=self.kwargs['username']
        )

        posts = Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(
            author=self.profile,
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

        if self.request.user != self.profile:
            posts = posts.filter(
                pub_date__lte=timezone.now(),
                category__is_published=True,
                is_published=True,
            ).annotate(
                comment_count=Count('comments')
            ).order_by('-pub_date')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = '__all__'
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        return Comment.objects.get(
            pk=self.kwargs['comment_pk'],
            post__pk=self.kwargs['pk']
        )

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    fields = '__all__'
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        return Comment.objects.get(
            pk=self.kwargs['comment_pk'],
            post__pk=self.kwargs['pk']
        )

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.object.post.pk})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = '__all__'
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user
    success_url = reverse_lazy('blog:index')


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.object.pk})


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        posts = Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
        return posts


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        posts = Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category=self.category
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_queryset(self):
        post = Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(
            pub_date__lte=timezone.now(),
            category__is_published=True
        )
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context
