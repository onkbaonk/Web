from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from forum.models import Thread
from blog.models import Post
from .models import Report


@login_required
def report_thread(request, thread_id):

    thread = get_object_or_404(Thread, id=thread_id)

    if request.method == "POST":
        reason = request.POST.get("reason")

        Report.objects.create(
            reporter=request.user,
            thread=thread,
            reason=reason,
        )

        return redirect("forum_home")

    return render(request, "moderation/report_thread.html", {
        "thread": thread
    })