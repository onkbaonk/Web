from django.utils import timezone
from chat.models import Message


def greeting(request):
    now = timezone.localtime()
    hour = now.hour

    if hour < 5:
        text = "Selamat Dini Hari 🌙"
    elif hour < 11:
        text = "Selamat Pagi ☀️"
    elif hour < 15:
        text = "Selamat Siang 🌤"
    elif hour < 18:
        text = "Selamat Sore 🌇"
    else:
        text = "Selamat Malam 🌙"

    if request.user.is_authenticated:
        message = f"{text}! {request.user.username}, Selamat Datang"
    else:
        message = f"{text}! Tamu, Selamat Datang"

    return {"greeting_text": message}

def message_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(
            conversation__participants=request.user,
            is_read=False
        ).exclude(sender=request.user).count()
    else:
        count = 0

    return {
        "message_count": count
    }