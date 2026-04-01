from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import User, Follow
from .forms import UserSettingsForm
from blog.models import Post
from forum.models import Thread, Reply
from itertools import chain
from operator import attrgetter
from notifications.models import Notification
from django.db.models import Q, Max, Count, F, FloatField, ExpressionWrapper
from django.utils.timezone import now
from datetime import timedelta
from django.contrib import messages


def home(request):

    # ================= FOLLOWING POSTS =================
    following_posts = Post.objects.none()

    if request.user.is_authenticated:

        following_ids = request.user.following.values_list(
            "following_id",
            flat=True
        )

        following_posts = Post.objects.filter(
            author__id__in=following_ids,
            status="published"
        )

    # ================= TRENDING BLOG =================
    last_7_days = now() - timedelta(days=7)

    trending_posts = Post.objects.filter(
        status="published",
        created_at__gte=last_7_days
    ).annotate(
        like_count=Count("likes"),
        comment_count=Count("comments"),
        score=ExpressionWrapper(
            F("views") * 0.4 +
            F("like_count") * 2 +
            F("comment_count") * 3,
            output_field=FloatField()
        )
    ).order_by("-score")

    # ================= DISCOVER BLOG =================
    discover_posts = Post.objects.filter(
        status="published"
    ).order_by("-created_at")

    # ================= FORUM THREAD =================
    threads = Thread.objects.select_related(
        "author",
        "category"
    ).order_by("-created_at")

     # ================= MIX FEED =================
    feed_items = list(following_posts) + list(trending_posts) + list(threads) + list(discover_posts)

    # ================= REMOVE DUPLICATE & ADD TYPE =================
    seen = set()
    feed = []
    for item in feed_items:
        key = f"{item.__class__.__name__}-{item.id}"
        if key not in seen:
            # Tambahkan penanda tipe agar template mudah mengenali
            item.is_post = isinstance(item, Post) 
            feed.append(item)
            seen.add(key)

    # ================= PAGINATION =================
    page = request.GET.get('page', 1)
    paginator = Paginator(feed, 10)  # Tampilkan 10 item per load

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = []

    # Jika request berasal dari AJAX, kirimkan partial saja
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, "partials/feed_items.html", {"feed": items})

    return render(request, "home.html", {"feed": items})

def register_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validasi kosong
        if not username or not password1 or not password2:
            return render(request, "accounts/register.html", {
                "error": "Semua field wajib diisi"
            })

        # Validasi password sama
        if password1 != password2:
            return render(request, "accounts/register.html", {
                "error": "Password tidak sama"
            })

        # Username unik
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                "error": "Username sudah digunakan"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)
        return redirect("home")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {"error": "Username atau password salah"})

    return render(request, 'login.html')

def custom_login(request):

    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect("login")

        if user.is_banned:
            messages.error(request, "Your account has been banned.")
            return redirect("login")

        login(request, user)
        return redirect("home")

    return render(request,"accounts/login.html")

def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    
    threads_count = Thread.objects.filter(author=user_profile).count()
    
    user_threads = Thread.objects.filter(author=user_profile).order_by('-created_at')
    user_replies = Reply.objects.filter(author=user_profile)
    posts = Post.objects.filter(
        author=user_profile,
        status="published"
    )
    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user_profile
        ).exists()
    history_list = sorted(
        chain(posts, user_threads, user_replies),
        key=attrgetter('created_at'),
        reverse=True
    )[:15] # Ambil 15 aktivitas terakhir
    
    context = {
        "user_profile": user_profile,
        'threads_count': threads_count,
        'user_threads': user_threads,
        "posts": posts,
        "is_following": is_following,
        "history_list": history_list,
    }
    
    return render(request, "accounts/profile.html", context)

@login_required
def settings_view(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
    else:
        form = UserSettingsForm(instance=request.user)
    return render(request, 'accounts/settings.html', {'form': form})

User = get_user_model()
def members_list(request):

    query = request.GET.get("q")

    users = User.objects.exclude(id=request.user.id)

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(bio__icontains=query) |
            Q(location__icontains=query)
        )

    following_usernames = []

    if request.user.is_authenticated:
        following_usernames = Follow.objects.filter(
            follower=request.user
        ).values_list("following__username", flat=True)

    context = {
        "users": users,
        "following_usernames": following_usernames,
        "query": query,
    }

    return render(request, "accounts/members.html", context)

@login_required
def toggle_follow(request, username):
    
    if request.method != "POST":
        return JsonResponse({"success": False})

    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return JsonResponse({"success": False})

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if not created:
        follow.delete()
        return JsonResponse({
            "success": True,
            "following": False
        })

    # ✅ notification
    Notification.objects.get_or_create(
        user=target_user,
        sender=request.user,
        notif_type="follow"
    )

    return JsonResponse({
        "success": True,
        "following": True
    })

@login_required
def followers_list(request, username):
    user_profile = get_object_or_404(User, username=username)

    followers = Follow.objects.filter(
        following=user_profile
    ).select_related("follower")

    html = render_to_string(
        "accounts/partials/follow_list.html",
        {
            "users": [f.follower for f in followers],
            "title": "Followers"
        },
        request=request
    )

    return JsonResponse({"html": html})


@login_required
def following_list(request, username):
    user_profile = get_object_or_404(User, username=username)

    following = Follow.objects.filter(
        follower=user_profile
    ).select_related("following")

    html = render_to_string(
        "accounts/partials/follow_list.html",
        {
            "users": [f.following for f in following],
            "title": "Following"
        },
        request=request
    )

    return JsonResponse({"html": html})

def load_more_posts(request):

    page = request.GET.get("page", 1)

    posts = Post.objects.filter(
        status="published"
    ).order_by("-created_at")

    paginator = Paginator(posts, 5)

    page_obj = paginator.get_page(page)

    html = render_to_string(
        "partials/post_list.html",
        {"posts": page_obj},
        request=request
    )

    return JsonResponse({
        "html": html,
        "has_next": page_obj.has_next()
    })

def logout_view(request):
    logout(request)
    return redirect('home')