from django.db import models


class Respondents(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=36, unique=True, null=False, blank=False)
    sex = models.CharField(max_length=1, null=False, blank=False)
    age = models.SmallIntegerField(null=False, blank=False)


class SpeakerNames(models.Model):
    speaker_name = models.CharField(max_length=100, null=False, blank=False)


class ModelNames(models.Model):
    model_name = models.CharField(max_length=100, null=False, blank=False)


class SampleNames(models.Model):
    sample_name = models.CharField(max_length=100, null=False, blank=False)


class Kinds(models.Model):
    kind = models.CharField(max_length=100, null=False, blank=False)


class Answers(models.Model):
    respondent = models.ForeignKey(Respondents, on_delete=models.CASCADE)
    speaker_name = models.ForeignKey(SpeakerNames, on_delete=models.CASCADE)
    model_name = models.ForeignKey(ModelNames, on_delete=models.CASCADE)
    sample_name = models.ForeignKey(SampleNames, on_delete=models.CASCADE)
    kind = models.ForeignKey(Kinds, on_delete=models.CASCADE)
    naturalness = models.SmallIntegerField(null=False, blank=False)
    intelligibility = models.SmallIntegerField(null=False, blank=False)
