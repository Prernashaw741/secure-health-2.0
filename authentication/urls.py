from django.urls import path
from .views import loginView, RegisterView , ForgotPasswordView
urlpatterns = [
    path("login/", loginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("forgotpassword/", ForgotPasswordView.as_view())
]
