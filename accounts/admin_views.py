from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from .models import AdminLog
from blog.models import Post
from forum.models import Thread
from .utils import admin_required
from django.contrib import messages
from moderation.models import Report

User = get_user_model()

@admin_required
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)
    
@admin_required
def admin_dashboard(request):

    context = {
        "user_count": User.objects.count(),
        "post_count": Post.objects.count(),
        "thread_count": Thread.objects.count(),
    }

    return render(request, "admin/dashboard.html", context)


@admin_required
def manage_users(request):
    users = User.objects.all().order_by("-date_joined")
    return render(request, "admin/users.html", {"users": users})


@admin_required
def manage_posts(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "admin/posts.html", {"posts": posts})

@admin_required
def manage_threads(request):
    threads = Thread.objects.all().order_by("-created_at")
    return render(request, "admin/threads.html", {
        "threads": threads
    })

@admin_required
def change_user_role(request, user_id, role):

    user = get_object_or_404(User, id=user_id)

    if role in ["member", "moderator", "admin"]:
        user.role = role
        user.save()
        messages.success(request, "Role updated")
        
    # ✅ LOG
    AdminLog.objects.create(
        admin=request.user,
        target_user=user,
        action="role_change",
        description=f"{request.user.username} changed role {user.username} to {new_role}"
    )
    return redirect("manage_users")

@admin_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("❌ Tidak diizinkan")
        
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        return HttpResponseForbidden("❌ Superuser tidak bisa dihapus")
        user.delete()
        messages.success(request, "User deleted")

    # ✅ LOG
    AdminLog.objects.create(
        admin=request.user,
        target_user=user,
        action="delete",
        description=f"{request.user.username} deleted {user.username}"
    )
    
    return redirect("manage_users")

@admin_required
def toggle_post_status(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if post.status == "published":
        post.status = "draft"
    else:
        post.status = "published"

    post.save()

    return redirect("manage_posts")


@admin_required
def delete_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    post.delete()

    return redirect("manage_posts")

@admin_required
def ban_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("❌ Tidak diizinkan")
        
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        return HttpResponseForbidden("❌ Superuser tidak bisa di-ban")

    user.is_banned = True
    user.save()

    # ✅ LOG
    AdminLog.objects.create(
        admin=request.user,
        target_user=user,
        action="ban",
        description=f"{request.user.username} banned {user.username}"
    )
    
    return redirect("manage_users")

@admin_required
def unban_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("❌ Tidak diizinkan")
        
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        return HttpResponseForbidden("❌ Superuser tidak bisa diubah")

    user.is_banned = False
    user.save()

    return redirect("manage_users")
def admin_logs(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("❌ Tidak diizinkan")

    logs = AdminLog.objects.all().order_by('-created_at')

    return render(request, 'admin/admin_logs.html', {
        'logs': logs
    })
@admin_required
def moderation_queue(request):
    reports = Report.objects.filter(status="pending").order_by("-created_at")
    return render(request, "admin/reports.html", {"reports": reports})
