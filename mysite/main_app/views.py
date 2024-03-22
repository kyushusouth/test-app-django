from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.shortcuts import get_list_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import (
    EvaluationForm,
    SignUpForm,
)
from .models import Answers, Respondents, SampleMetaData


class SignupView(LoginRequiredMixin, CreateView):
    form_class = SignUpForm
    template_name = "main_app/signup.html"
    success_url = reverse_lazy("main_app:index")


class RespondentInfoCreateView(LoginRequiredMixin, UpdateView):
    model = Respondents
    fields = ["sex", "age"]
    template_name = "main_app/respondent_info.html"
    success_url = reverse_lazy("main_app:index")


class CheckRespondentsView(LoginRequiredMixin, ListView):
    model = Respondents
    template_name = "main_app/check_respondents.html"
    context_object_name = "respondents_list"
    paginate_by = 10


class CheckAnswersView(LoginRequiredMixin, ListView):
    model = Answers
    template_name = "main_app/check_answers.html"
    context_object_name = "answers_list"
    paginate_by = 10


@require_http_methods(["GET"])
def index(request):
    if request.user.is_authenticated:
        return render(request, "main_app/index.html")
    else:
        return redirect("main_app:login")


@login_required
@require_http_methods(["GET", "POST"])
def eval(request):
    metadata_list = get_list_or_404(SampleMetaData)
    metadata_list = metadata_list[:3]
    urls = [x.file_path.url for x in metadata_list]
    AnswerFormSet = modelformset_factory(Answers, form=EvaluationForm, extra=len(urls))
    if request.method == "POST":
        formset = AnswerFormSet(request.POST)
        if formset.is_valid():
            respondent = Respondents.objects.get(username=request.user.username)
            for form in formset.cleaned_data:
                naturalness = form["naturalness"]
                intelligibility = form["intelligibility"]
                url = form["url"]
                file_path = url.split("/")[-1]
                sample_meta_data = SampleMetaData.objects.get(file_path=file_path)
                answer = Answers(
                    respondent=respondent,
                    sample_meta_data=sample_meta_data,
                    naturalness=naturalness,
                    intelligibility=intelligibility,
                )
                answer.save()
            return redirect("main_app:index")
        else:
            return render(request, "main_app/eval.html", {"formset": formset})
    else:
        data = {
            "form-TOTAL_FORMS": str(len(urls)),
            "form-INITIAL_FORMS": "0",
        }
        for i, url in enumerate(urls):
            data.update(
                {
                    f"form-{i}-url": url,
                    f"form-{i}-naturalness": "",
                    f"form-{i}-intelligibility": "",
                }
            )
        formset = AnswerFormSet(data)
        return render(request, "main_app/eval.html", {"formset": formset})
