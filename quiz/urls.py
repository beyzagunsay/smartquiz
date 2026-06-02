from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views, admin_views

urlpatterns = [
    path("", views.home, name="home"),
    path("leaderboard/", views.leaderboard_view, name="leaderboard"),
    path("profile/", views.profile_view, name="profile"),
    path("topics/", views.topics, name="topics"),
    path("quiz/<int:topic_id>/", views.quiz_view, name="quiz"),
    path("package/<int:topic_id>/", views.package_view, name="package"),
    path("register/", views.register_view, name="register"),

    path(
        "login/",
        LoginView.as_view(template_name="quiz/login.html"),
        name="login"
    ),

    path(
        "logout/",
        LogoutView.as_view(next_page="/"),
        name="logout"
    ),

    
path("dashboard/", admin_views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/users/", admin_views.admin_users, name="admin_users"),
    path("dashboard/users/<int:user_id>/toggle/", admin_views.admin_user_toggle, name="admin_user_toggle"),
    path("dashboard/users/<int:user_id>/delete/", admin_views.admin_user_delete, name="admin_user_delete"),
    path("dashboard/users/<int:user_id>/staff/", admin_views.admin_user_make_staff, name="admin_user_make_staff"),
    path("dashboard/content/", admin_views.admin_content, name="admin_content"),
    path("dashboard/content/<int:topic_id>/toggle/", admin_views.admin_topic_toggle, name="admin_topic_toggle"),
    path("dashboard/content/<int:topic_id>/delete/", admin_views.admin_topic_delete, name="admin_topic_delete"),
]
