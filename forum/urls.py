from django.urls import path
from . import views

urlpatterns = [
    path("", views.forum_home, name="forum_home"),
    path('category/<int:pk>/', views.thread_list, name='thread_list'),
    path("thread/<int:pk>/", views.thread_detail, name="thread_detail"),
    path("thread/<int:pk>/reply/", views.add_reply, name="add_reply"),
]
