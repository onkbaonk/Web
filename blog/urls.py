from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.post_create, name='post_create'),
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/comment/', views.post_comment, name='post_comment'),
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('post/<slug:slug>/like/', views.toggle_like, name='toggle_like'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path("notifications/", views.notifications_dropdown, name="notifications_dropdown"),
    path('notifications/count/', views.notification_count, name='notification_count'),
    path(
    "comment/<int:comment_id>/replies/",
    views.load_replies,
    name="load_replies"
),
]
