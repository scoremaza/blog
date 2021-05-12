from django.core import paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from .models import Post, Comment

def post_share(request, post_id):
    '''
    Forms for email 
    ''' 
    #Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form fields passed validatation
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # From fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject  = f"{cd['name']} recommends you read "\
                f"{post.title}"
            message  = f"Read {post.title} at {post_url}\n\n"\
                f"{cd['name']}'\s comments: {cd['comments']}"
            send_mail(subject,message, 'johnny45gotu@gmail.com', [cd['to']])
            sent = True

    else: 
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent':sent})

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 4) # 3 posts in each page
    page      = request.GET.get('page')
  
    print('HEllo')
    try:
        posts     = paginator.page(page)
       
    except PageNotAnInteger:
        # If page is not an integer dieliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # IF page is out of range deliver last page results
        post = paginator.page(paginator.num_pages)
    
    return render(request,
                  'blog/post/list.html',
                 {'posts':posts,
                  'page':page})

class PostListView(ListView):
    '''
    Here we have a generic called a ListView it will create
    '''
    queryset   = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post 
            # Save the comment to the database
            new_comment.save()
        else:
            comment_form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  {'post':post,
                  'comments': comments,
                  'new_comment': new_comment,
                  'comment_form': comment_form})

# Create your views here.
