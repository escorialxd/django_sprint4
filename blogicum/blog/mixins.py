from .models import Comment, Post


class PostsQuerySetMixin:
    def get_queryset(self):
        return Post.post_list


class PostsMixin:
    model = Post
    template_name = "blog/create.html"
    queryset = Post.objects.select_related("author", "location", "category")


class CommentMixin:
    model = Comment
    pk_url_kwarg = "comment_pk"
    template_name = "blog/comment.html"
