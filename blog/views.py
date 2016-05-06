from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm

# Create your views here.


def post_list(request):
    # posts = Post.objects.filter(published_date__lt=timezone.now()).order_by('published_date')

    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    this_post = get_object_or_404(Post, pk=int(pk))
    return render(request, 'blog/post_detail.html', {'detail': this_post})


def post_new(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blog/post_new.html', {'form': form})
    else:
        # return redirect(post_list)
        if isinstance(request.user, AnonymousUser):
            return redirect(post_list)

        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, pk=post.pk)
        else:
            return redirect(post_new)


def post_edit(request, pk):
    if isinstance(request.user, AnonymousUser):
            return redirect(post_list)
    post = get_object_or_404(Post, pk=int(pk))
    if request.method == 'GET':

        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, pk=post.pk)
        else:
            return redirect(post_edit)


