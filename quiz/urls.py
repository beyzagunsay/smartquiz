from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("topics/", views.topics, name="topics"),

    path("quiz/<int:topic_id>/", views.quiz_view, name="quiz"),

    path("package/<int:topic_id>/", views.package_view, name="package"),

    path("register/", views.register_view, name="register"),

    path(
        "login/",
        LoginView.as_view(
            template_name="quiz/login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        LogoutView.as_view(next_page="/"),
        name="logout"
    ),
]