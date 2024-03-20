import random
import uuid

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView

from .forms import AnswerForm, UserForm
from .models import Answers, Respondents, SampleMetaData


@require_http_methods(["GET"])
def index(request):
    return render(request, "main_app/index.html")


@require_http_methods(["GET", "POST"])
def register_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            user.save()
            return redirect("main_app:check_user")
    else:
        form = UserForm()
        return render(request, "main_app/register_user.html", {"form": form})


class RegisterUserView(View):
    user_form_class = UserForm
    template_name_get = "main_app/register_user.html"
    redirect_dest_post = "main_app:check_user"

    def get(self, request, *args, **kwargs):
        form = self.user_form_class()
        return render(request, self.template_name_get, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.user_form_class(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            user.save()
            return redirect(self.redirect_dest_post)


class CheckUserView(ListView):
    model = User
    template_name = "main_app/check_user.html"
    context_object_name = "user_list"
    paginate_by = 10


@require_http_methods(["GET", "POST"])
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main_app:user_page", id=user.pk)
    else:
        form = UserForm()
        return render(request, "main_app/login_user.html", {"form": form})


@require_http_methods(["GET"])
def user_page(request, id: int, key1: str):
    user = get_object_or_404(User, pk=id)
    return render(request, "main_app/user_page.html", {"user": user, "key1": key1})


class CheckRespondentsView(ListView):
    model = Respondents
    template_name = "main_app/check_respondents.html"
    context_object_name = "respondents_list"
    paginate_by = 10


class CheckAnswersView(ListView):
    model = Answers
    template_name = "main_app/check_answers.html"
    context_object_name = "answers_list"
    paginate_by = 10


@require_http_methods(["GET"])
def thanks(request):
    return render(request, "main_app/thanks.html")


@require_http_methods(["GET", "POST"])
def eval(request):
    metadata = get_list_or_404(SampleMetaData)
    urls = [x.file_path.url for x in metadata]
    urls = urls[:5]
    AnswerFormSet = formset_factory(AnswerForm, extra=len(urls))
    if request.method == "POST":
        formset = AnswerFormSet(request.POST)
        if formset.is_valid():
            respondent = Respondents(
                name=uuid.uuid4(),
                sex=random.choice(["M", "F", "N"]),
                age=random.randint(1, 100),
            )
            respondent.save()
            for form in formset.cleaned_data:
                naturalness = form["naturalness"]
                intelligibility = form["intelligibility"]
                url = form["url"]
                file_name = url.split("/")[-1].split(".")[0]
                sample_meta_data = SampleMetaData.objects.get(file_name=file_name)
                answer = Answers(
                    respondent=respondent,
                    sample_meta_data=sample_meta_data,
                    naturalness=naturalness,
                    intelligibility=intelligibility,
                )
                answer.save()
            return redirect("main_app:thanks")
    else:
        data = {
            "form-TOTAL_FORMS": str(len(urls)),
            "form-INITIAL_FORMS": "0",
        }
        for i, url in enumerate(urls):
            data.update(
                {
                    f"form-{i}-intelligibility": "",
                    f"form-{i}-naturalness": "",
                    f"form-{i}-url": url,
                }
            )
        formset = AnswerFormSet(data)
        return render(request, "main_app/eval.html", {"formset": formset, "urls": urls})
