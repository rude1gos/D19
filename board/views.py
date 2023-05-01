from django.shortcuts import get_object_or_404

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Reply
from .forms import PostForm, ReplyForm
from .filters import PostFilter

from django.contrib.auth.mixins import PermissionRequiredMixin
# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 5

    # Переопределяем функцию получения списка статей
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reply_list_by_postid = Reply.objects.filter(post=self.kwargs['pk']).order_by('-date')
        context['replys'] = reply_list_by_postid
        return context

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        path = self.request.META['PATH_INFO']

        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = True
        return context

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_by_id = get_object_or_404(Post, id=self.kwargs['pk'])
        context['is_author'] = True if post_by_id.author == self.request.user else False
        return context

class ReplyAdd(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_reply')
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_add.html'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.user = self.request.user
        reply.post = get_object_or_404(Post, id=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_data = get_object_or_404(Post, id=self.kwargs['pk'])
        context['news'] = post_data
        return context