from django.urls import path
from . import views

urlpatterns = [
    path("report/thread/<int:thread_id>/", views.report_thread, name="report_thread"),
]
