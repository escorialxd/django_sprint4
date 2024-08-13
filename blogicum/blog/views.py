from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from .models import Post, Category, Comment, User
from .forms import CommentForm, PostForm, ProfileForm
from django.http import Http404


def index(request):
    posts = Post.objects.published()[:settings.PAGINATOR]
    context = {'post_list': posts}
    return render(request, 'blog/index.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    post_list = category.posts.published()
    context = {'category': category, 'post_list': post_list}
    return render(request, 'blog/category.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post.objects.published(), id=id)
    if post.pub_date > timezone.now():
        raise Http404('Пост не найден')
    form = CommentForm()
    comments = post.comments.select_related('author')
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'blog/detail.html', context)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('profile', username=request.user.username)
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'blog/post_form.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'blog/post_form.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('profile', username=request.user.username)
    context = {'post': post}
    return render(request, 'blog/confirm_delete.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.created_at = timezone.now()
            comment.save()
            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'blog/comment_form.html', context)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post_id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'blog/comment_form.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id, author=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', id=post_id)
    context = {'comment': comment}
    return render(request, 'blog/confirm_delete.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    context = {'profile': user, 'post_list': posts}
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'blog/user_form.html', context)
