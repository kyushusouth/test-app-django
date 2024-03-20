from django.urls import path

from . import views

app_name = "main_app"
urlpatterns = [
    path("", views.index, name="index"),
    path("eval", views.eval, name="eval"),
    path("thanks", views.thanks, name="thanks"),
    path(
        "check_respondents",
        views.CheckRespondentsView.as_view(),
        name="check_respondents",
    ),
    path("check_answers", views.CheckAnswersView.as_view(), name="check_answers"),
    path("register_user", views.RegisterUserView.as_view(), name="register_user"),
    path("check_user", views.CheckUserView.as_view(), name="check_user"),
    path("login_user", views.login_user, name="login_user"),
    path("user/<str:id>", views.user_page, {"key1": "value1"}, name="user_page"),
]
