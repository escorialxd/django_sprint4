from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import Comment, Post
from .forms import CreatePostForm, CreateCommentForm
from django.contrib.auth import get_user_model

User = get_user_model()


class PostsMixin:
    model = Post
    template_name = "blog/create.html"
    queryset = Post.objects.select_related("author", "location", "category")
    form_class = CreatePostForm


class CommentMixin:
    model = Comment
    form_class = CreateCommentForm
    pk_url_kwarg = "comment_pk"
    template_name = "blog/comment.html"


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return redirect('blog:post_detail', pk=self.object.pk)
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteUpdateMixin:
    def get_object(self, queryset=None):
        obj = get_object_or_404(Comment, pk=self.kwargs["comment_pk"])
        if self.request.user != obj.author:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.object
        return context
