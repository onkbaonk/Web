from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from django.http import JsonResponse
import json
from django.db.models import Max, Count, Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required
def start_conversation(request, username):
    other_user = get_object_or_404(User, username=username)

    if other_user == request.user:
        return redirect("profile", username=username)

    # Cari conversation yang sudah ada
    conversations = Conversation.objects.filter(participants=request.user)

    for convo in conversations:
        if convo.participants.filter(id=other_user.id).exists():
            return redirect("conversation_detail", convo.id)

    # Kalau belum ada → buat baru
    convo = Conversation.objects.create()
    convo.participants.add(request.user, other_user)

    return redirect("conversation_detail", convo.id)

@login_required
def conversation_detail(request, convo_id):
    conversation = get_object_or_404(Conversation, id=convo_id)
    
    if request.user not in conversation.participants.all():
        return redirect("activity_feed")

    # mark as read
    conversation.messages.filter(
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )

    chat_messages = conversation.messages.all()
    conversations = Conversation.objects.filter(
        participants=request.user
      )

    return render(request, "chat/conversation_detail.html", {
        "conversation": conversation,
        "conversations":conversations,
        "chat_messages": chat_messages
    })

@login_required
def inbox_view(request):
    conversations = Conversation.objects.filter(
        participants=request.user
    ).annotate(
        last_message_time=Max("messages__created_at"),
        unread_count=Count(
            "messages",
            filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user)
        )
    ).order_by("-last_message_time", "-created_at")

    return render(request, "chat/inbox.html", {
        "conversations": conversations
    })

@login_required
def send_message_ajax(request, convo_id):
    if request.method == "POST":
        content = request.POST.get("content")

        conversation = Conversation.objects.get(id=convo_id)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        
        # 🔥 BROADCAST KE WEBSOCKET
        channel_layer = get_channel_layer()

        print(f"Mengirim ke grup: chat_{conversation.id}")
        async_to_sync(channel_layer.group_send)(
            f"chat_{conversation.id}",
            {
                "type": "chat_message",
                "type": "read_update",
                "message": message.content,
                "sender": request.user.username,
                "time": message.created_at.strftime("%H:%M"),
            }
        )
        print("Berhasil kirim ke group_send")

        return JsonResponse({
            "message": message.content,
            "time": message.created_at.strftime("%H:%M"),
        })

@login_required
def edit_message(request, pk):
    message = get_object_or_404(Message, id=pk)
    
    # Pastikan hanya pengirim yang bisa edit
    if message.sender != request.user:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

    if request.method == "POST":
        # Ambil data dari AJAX
        new_content = request.POST.get('content')
        if new_content:
            message.content = new_content
            message.save()
            return JsonResponse({
                'status': 'success', 
                'content': message.content
            })
            
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_message(request, pk):
    msg = get_object_or_404(Message, id=pk, sender=request.user)
    msg.delete()
    return JsonResponse({'status': 'deleted'})

@login_required
def clear_chat(request, pk):

    conversation = get_object_or_404(Conversation, id=pk)

    conversation.messages.all().delete()

    return redirect("conversation_detail", pk)

@login_required
def delete_conversation(request, pk):

    conversation = get_object_or_404(
        Conversation,
        id=pk,
        participants=request.user
    )

    conversation.delete()

    return redirect("/")

def get_messages(request, convo_id):
    conversation = Conversation.objects.get(id=convo_id)

    messages = Message.objects.filter(conversation=conversation).order_by("created_at")

    data = []
    for m in messages:
        data.append({
            "id": m.id,
            "sender": m.sender.username,
            "content": m.content,
            "time": m.created_at.strftime("%H:%M"),
            "is_me": m.sender == request.user
        })

    return JsonResponse({"messages": data})
