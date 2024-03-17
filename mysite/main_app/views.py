import random
import uuid
from pathlib import Path

from django.contrib.staticfiles import finders
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import AnswerForm
from .models import Answers, Kinds, ModelNames, Respondents, SampleNames, SpeakerNames


def get_wav_files():
    result = finders.find("main_app/wav_files")
    urls = list(Path(result).glob("**/*.wav"))
    urls = ["/".join(url.parts[-8:]) for url in urls]   
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
                url_split = url.split("/")
                speaker_name = url_split[-3]
                model_name = url_split[-5]
                sample_name = url_split[-2]
                kind = url_split[-1].split(".wav")[0]

                speaker_name = SpeakerNames.objects.get(
                    speaker_name=speaker_name,
                )
                model_name = ModelNames.objects.get(
                    model_name=model_name,
                )
                sample_name = SampleNames.objects.get(
                    sample_name=sample_name,
                )
                kind = Kinds.objects.get(
                    kind=kind,
                )
                answer = Answers(
                    respondent=respondent,
                    speaker_name=speaker_name,
                    model_name=model_name,
                    sample_name=sample_name,
                    kind=kind,
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
