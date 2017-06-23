from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .forms import PostForm

User = get_user_model()


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'post/post_list.html', context=context)


def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    else:
        return render(request, 'post/post_delete.html')


def post_modify(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.first()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    context = {
        'form': form
    }
    return render(request, 'post/post_modify.html', context=context)
