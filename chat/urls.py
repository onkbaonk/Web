from django.urls import path
from . import views

urlpatterns = [
    path("", views.inbox_view, name="inbox"),
    path("start/<str:username>/", views.start_conversation, name="start_conversation"),
    path("<int:convo_id>/", views.conversation_detail, name="conversation_detail"),
    path("send/<int:convo_id>/", views.send_message_ajax, name="send_message_ajax"),
    path("delete-message/<int:pk>/", views.delete_message, name="delete_message"),
    path("clear-chat/<int:pk>/", views.clear_chat, name="clear_chat"),
    path("delete-conversation/<int:pk>/", views.delete_conversation, name="delete_conversation"),
    path("chat/<int:convo_id>/messages/", views.get_messages, name="get_messages"),
    path("edit-message/<int:pk>/", views.edit_message, name="edit_message"),
]