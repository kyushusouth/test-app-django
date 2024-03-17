from django.urls import path

from . import views

app_name = "main_app"
urlpatterns = [
    path("", views.index, name="index"),
    path("eval", views.eval, name="eval"),
    path("thanks", views.thanks, name="thanks"),
    path("respondents", views.respondents, name="respondents"),
    path("answers", views.answers, name="answers"),
]
