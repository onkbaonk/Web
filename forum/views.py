from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReplyForm
from .models import Thread, Category, Reply
from django.db.models import Count


def forum_home(request):
    categories = Category.objects.all()
    threads = Thread.objects.select_related("author", "category").order_by("-created_at")

    context = {
        "categories": categories,
        "threads": threads,
    }
    return render(request, "forum/home.html", context)

def thread_list(request, pk):
    category = get_object_or_404(ForumCategory, pk=pk)
    # AMBIL DATA DARI DATABASE:
    threads = Thread.objects.filter(category=category).order_by('-created_at')
    
    return render(request, 'forum/thread_list.html', {
        'category': category,
        'threads': threads  # DATA INI WAJIB ADA
    })

def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    replies = thread.replies.filter(parent__isnull=True).order_by("created_at")

    form = ReplyForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.thread = thread
            reply.save()
            return redirect("thread_detail", pk=thread.pk)

    context = {
        "thread": thread,
        "replies": replies,
        "form": form,
    }

    return render(request, "forum/thread_detail.html", context)

@login_required
def add_reply(request, pk):
    thread = get_object_or_404(Thread, pk=pk)

    if request.method == "POST":
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")

        parent_obj = None
        if parent_id:
            parent_obj = get_object_or_404(Reply, id=parent_id)
        
        Reply.objects.create(
            thread=thread,
            author=request.user,
            content=content,
            parent=parent_obj
        )

    return redirect("thread_detail", pk=thread.pk)
