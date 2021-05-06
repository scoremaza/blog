from django.core import paginator
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from .models import Post


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page      = request.GET.get('page')
    try:
        posts     = Post.published.all()
    except PageNotAnInteger:
        # If page is not an integer dieliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # IF page is out of range deliver last page results
        post = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'posts':posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post':post})

# Create your views here.
