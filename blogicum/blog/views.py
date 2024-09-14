from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .constants import PAGINATOR
from .forms import CreateCommentForm, CreatePostForm
from .models import Category, Comment, Post
from .mixins import (
    CommentMixin,
    PostsMixin,
    OwnerRequiredMixin,
    CommentDeleteUpdateMixin,
)

User = get_user_model()


class PostDeleteView(OwnerRequiredMixin, PostsMixin,
                     LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy("blog:index")


class PostUpdateView(OwnerRequiredMixin, PostsMixin,
                     LoginRequiredMixin, UpdateView):
    form_class = CreatePostForm

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


class PostCreateView(PostsMixin, LoginRequiredMixin, CreateView):
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "blog:profile",
            kwargs={
                "username": self.request.user.username,
            },
        )


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_published and obj.author != self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreateCommentForm()
        context["comments"] = (
            self.object.comments.prefetch_related("author").all()
        )
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CreateCommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs["pk"]})


class CommentDeleteView(
    CommentMixin, CommentDeleteUpdateMixin, LoginRequiredMixin, DeleteView
):
    template_name = "blog/comment.html"


class CommentUpdateView(
    CommentMixin, CommentDeleteUpdateMixin, LoginRequiredMixin, UpdateView
):
    template_name = "blog/comment.html"


class ProfileListView(ListView):
    model = Post
    template_name = "blog/profile.html"
    paginate_by = PAGINATOR

    def get_author(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_queryset(self):
        author = self.get_author()
        return (
            author.posts.all()
            .with_related()
            .with_comment_count()
            .order_by_date()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_author()
        return context


class IndexListView(PostsMixin, ListView):
    template_name = "blog/index.html"
    context_object_name = "post_list"
    paginate_by = PAGINATOR

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .published()
            .with_related()
            .with_comment_count()
            .order_by_date()
        )


class CategoryListView(ListView):
    model = Post
    template_name = "blog/category.html"
    context_object_name = "post_list"
    paginate_by = PAGINATOR

    def get_category(self):
        return get_object_or_404(
            Category, slug=self.kwargs["category_slug"], is_published=True
        )

    def get_queryset(self):
        category = self.get_category()
        return (
            category.posts.all()
            .published()
            .with_related()
            .with_comment_count()
            .order_by_date()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.get_category()
        return context
