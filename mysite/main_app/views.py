import random
import uuid
from pathlib import Path

from django.contrib.staticfiles import finders
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import AnswerForm
from .models import Answers, Respondents, SampleMetaData


def get_wav_files():
    result = finders.find("main_app/wav_files_encrypted")
    urls = list(Path(result).glob("*.wav"))
    urls = ["/".join(url.parts[-3:]) for url in urls]
    urls = urls[:2]
    return urls


def index(request):
    return render(request, "main_app/index.html")


def respondents(request):
    all_respondents = Respondents.objects.all()
    return render(request, "main_app/respondents.html", {"all_respondents": all_respondents})


def answers(request):
    all_answers = Answers.objects.all()
    return render(request, "main_app/answers.html", {"all_answers": all_answers})


def thanks(request):
    return render(request, "main_app/thanks.html")


def eval(request):
    urls = get_wav_files()
    AnswerFormSet = formset_factory(AnswerForm, extra=len(urls))
    if request.method == "POST":
        formset = AnswerFormSet(request.POST, request.FILES)
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
                sample_meta_data = SampleMetaData.objects.get(
                    file_name=file_name
                )
                answer = Answers(
                    respondent=respondent,
                    sample_meta_data=sample_meta_data,
                    naturalness=naturalness,
                    intelligibility=intelligibility,
                )
                answer.save()
            return HttpResponseRedirect("/main_app/thanks")
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
        urls = get_wav_files()
        return render(request, "main_app/eval.html", {"formset": formset, "urls": urls})
