from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notifications'),
    path("", views.notification_list, name="notification_list"),
    path("clear/", views.clear_notifications, name="clear_notifications"),
    path("delete/<int:pk>/", views.delete_notification, name="delete_notification"),
]
