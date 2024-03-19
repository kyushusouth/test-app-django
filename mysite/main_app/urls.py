from django.urls import path

from . import views

app_name = "main_app"
urlpatterns = [
    path(
        "",
        views.index,
        {"year_list": [2000, 2001, 2002, 2003, 2004, 2005, 2006]},
        name="index",
    ),
    path("eval", views.eval, name="eval"),
    path("thanks", views.thanks, name="thanks"),
    path("respondents", views.respondents, name="respondents"),
    path("answers", views.answers, name="answers"),
    path("register_user", views.register_user, name="register_user"),
    path("check_user", views.check_user, name="check_user"),
    path("login_user", views.login_user, name="login_user"),
    path("user/<str:id>", views.user_page, {"key1": "value1"}, name="user_page"),
    path("articles/<int:year>", views.news_year_archive, name="news_year_archive"),
]
