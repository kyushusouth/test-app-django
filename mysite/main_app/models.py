from django.db import models


class Respondents(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=36, unique=True, null=False, blank=False)
    sex = models.CharField(max_length=1, null=False, blank=False)
    age = models.SmallIntegerField(null=False, blank=False)


class SampleMetaData(models.Model):
    file_name = models.CharField(max_length=36, unique=True, null=False, blank=False)
    speaker_name = models.CharField(max_length=100, null=False, blank=False)
    model_name = models.CharField(max_length=100, null=False, blank=False)
    sample_name = models.CharField(max_length=100, null=False, blank=False)
    kind = models.CharField(max_length=100, null=False, blank=False)


class Answers(models.Model):
    respondent = models.ForeignKey(Respondents, on_delete=models.CASCADE)
    sample_meta_data = models.ForeignKey(SampleMetaData, on_delete=models.CASCADE)
    naturalness = models.SmallIntegerField(null=False, blank=False)
    intelligibility = models.SmallIntegerField(null=False, blank=False)
