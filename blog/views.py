from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Comment, PostLike
from django.contrib import messages
from .forms import PostForm
from django.db.models import F, Q
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from notifications.models import Notification

def post_list(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(
            Q(status='published') |
            Q(author=request.user)
        ).order_by('-created_at')
    else:
        posts = Post.objects.filter(
            status='published'
        ).order_by('-created_at')

    paginator = Paginator(posts, 6)  # 6 post per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'posts': posts
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Draft protection
    if post.status == 'draft':
        if not request.user.is_authenticated:
            raise Http404()
        if request.user != post.author and not request.user.is_staff:
            raise Http404()

    # safe view increment
    Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
    post.refresh_from_db()

    comments = post.comments.filter(parent__isnull=True, is_active=True)

    related_posts = Post.objects.filter(
        category=post.category,
        status='published'
    ).exclude(id=post.id)[:3]

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')

    content = request.POST.get('content')
    parent_id = request.POST.get('parent_id')

    parent = None
    if parent_id and parent_id.isdigit():
        try:
            parent = Comment.objects.get(id=int(parent_id))
        except Comment.DoesNotExist:
            parent = None

    comment = Comment.objects.create(
        post=post,
        author=request.user,
        content=content,
        parent=parent
    )
    
    # ================= NOTIFICATION =================
    
    # reply notification
    if parent and parent.author != request.user:
      Notification.objects.create(
          user=parent.author,
          sender=request.user,
          notif_type='reply',
          post_slug=post.slug
      )
      
      # comment notification (author post)
    elif post.author != request.user:
        Notification.objects.create(
          user=post.author,
          sender=request.user,
          notif_type='comment',
          post_slug=post.slug
        )

    html = render_to_string(
        "blog/partials/comment_item.html",
        {"comment": comment, "user": request.user},
        request=request
    )

    return JsonResponse({
        "success": True,
        "html": html,
        "parent_id": parent.id if parent else None,
    })

@login_required
def load_replies(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)

    replies = comment.replies.filter(is_active=True)

    html = render_to_string(
        "blog/partials/reply_list.html",
        {"replies": replies},
        request=request
    )

    return JsonResponse({"html": html})

@login_required
def notifications_dropdown(request):

    # queryset asli (BELUM slice)
    qs = request.user.notifications.all()

    # ambil 10 untuk dropdown
    notifications = qs[:4]

    html = render_to_string(
        "blog/partials/notification_list.html",
        {"notifications": notifications},
        request=request
    )

    # mark read (pakai queryset asli)
    qs.filter(is_read=False).update(is_read=True)

    return JsonResponse({"html": html})

@login_required
def notification_count(request):
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({"count": count})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # Security check
    if request.user == comment.author or request.user.is_staff:
        post_url = comment.post.get_absolute_url()
        comment.delete()
        return redirect(post_url)

    return redirect('post_list')

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # SECURITY
    if request.user != post.author and not request.user.is_staff:
        return HttpResponseForbidden("Tidak diizinkan")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {
        'form': form,
        'edit_mode': True
    })

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author and not request.user.is_staff:
        return HttpResponseForbidden("Tidak diizinkan")

    if request.method == "POST":
        post.delete()
        return redirect('post_list')

    return render(request, 'blog/post_confirm_delete.html', {
        'post': post
    })

@login_required
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)

    like, created = PostLike.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        like.delete()
    else:
        if post.author != request.user:
            Notification.objects.create(
                user=post.author,
                sender=request.user,
                notif_type="like",
                post_slug=post.slug
            )
    
    return redirect(post.get_absolute_url())
