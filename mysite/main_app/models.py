from django.contrib.auth.models import AbstractUser
from django.db import models


class Sex(models.Model):
    kind = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.kind


class Respondents(AbstractUser):
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE, null=True, blank=True)
    age = models.SmallIntegerField(null=True, blank=True)
    # is_answerd_form_respondent_info = models.BooleanField(null=True, blank=True)
    # is_answerd_form_eval = models.BooleanField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.username


class SampleMetaData(models.Model):
    file_path = models.FileField(upload_to="", unique=True)
    speaker_name = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    sample_name = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.file_path.url


class NaturalnessItems(models.Model):
    item = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.pk}: {self.item}"


class IntelligibilityItems(models.Model):
    item = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.pk}: {self.item}"


class Answers(models.Model):
    respondent = models.ForeignKey(Respondents, on_delete=models.CASCADE)
    sample_meta_data = models.ForeignKey(SampleMetaData, on_delete=models.CASCADE)
    naturalness = models.ForeignKey(NaturalnessItems, on_delete=models.CASCADE)
    intelligibility = models.ForeignKey(IntelligibilityItems, on_delete=models.CASCADE)
