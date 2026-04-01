from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def notification_list(request):
    notifications = request.user.notifications.all()

    # mark read
    notifications.update(is_read=True)

    return render(request, "notifications/list.html", {
        "notifications": notifications
    })
    
@login_required
def clear_notifications(request):
    request.user.notifications.all().delete()
    return redirect("notification_list")

@login_required
def delete_notification(request, pk):
    notif = request.user.notifications.filter(pk=pk).first()

    if notif:
        notif.delete()

    return redirect("notification_list")