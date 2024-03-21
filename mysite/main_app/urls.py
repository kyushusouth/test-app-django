from django.contrib.auth import views as auth_views
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
    path("user_page", views.user_page, name="user_page"),
    path(
        "login",
        auth_views.LoginView.as_view(
            template_name="main_app/login.html", next_page="main_app:user_page"
        ),
        name="login",
    ),
    path(
        "logout",
        auth_views.LogoutView.as_view(next_page="main_app:login"),
        name="logout",
    ),
    path("signup", views.SignupView.as_view(), name="signup"),
    path(
        "answer_respondent_info/<int:pk>",
        views.RespondentInfoCreateView.as_view(),
        name="answer_respondent_info",
    ),
]
