from django.urls import path
from . import views
from .views import settings_view
from . import admin_views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.custom_login, name="login"),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', settings_view, name='settings'),
    path("u/<str:username>/", views.profile_view, name="profile"),
    path("members/", views.members_list, name="members"),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path("followers/<str:username>/", views.followers_list, name="followers_list"),
    path("following/<str:username>/", views.following_list, name="following_list"),
    path("load-posts/", views.load_more_posts, name="load_posts"),
    path("admin-dashboard/", admin_views. admin_dashboard, name="admin_dashboard"),
    path("admin/users/", admin_views.manage_users, name="manage_users"),
    path("admin/posts/", admin_views.manage_posts, name="manage_posts"),
    path("admin/threads/", admin_views.manage_threads, name="manage_threads"),
    path("admin/user/<int:user_id>/delete/", admin_views.delete_user, name="delete_user"),
    path("admin/user/<int:user_id>/role/<str:role>/", admin_views.change_user_role, name="change_user_role"),
    path("admin/post/<int:post_id>/toggle/", admin_views.toggle_post_status, name="toggle_post_status"),
    path("admin/post/<int:post_id>/delete/", admin_views.delete_post, name="delete_post"),
    path("admin/user/<int:user_id>/ban/", admin_views.ban_user, name="ban_user"),
    path("admin/user/<int:user_id>/unban/", admin_views.unban_user, name="unban_user"),
    path("admin/reports/", admin_views.moderation_queue, name="moderation_queue"),
    path("admin/logs/", admin_views.admin_logs, name='admin_logs'),
]