from django.urls import path
from .views import StudentApplicationCreateView, JobApplicationCreateView,ContactListCreateAPIView

urlpatterns = [
    path('student/', StudentApplicationCreateView.as_view(), name='api_student'),
    path('job/', JobApplicationCreateView.as_view(), name='api_job'),
    path("contact/", ContactListCreateAPIView.as_view(), name="api_contact"),
]
