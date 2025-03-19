from django.urls import path
from .views import ContactView, SignupView

urlpatterns = [
    path("contact/", ContactView.as_view(), name="contact"),
    path("signup/", SignupView.as_view(), name="signup"),
]
