from django.db import models


# class CustomUser(AbstractUser):
#     sex = models.CharField(max_length=1, null=False, blank=False)
#     age = models.SmallIntegerField(null=False, blank=False)


class Respondents(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=36, unique=True)
    sex = models.CharField(max_length=1)
    age = models.SmallIntegerField()


class SampleMetaData(models.Model):
    file_path = models.FileField(upload_to="")
    file_name = models.CharField(max_length=36, unique=True)
    speaker_name = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    sample_name = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.file_path.url


class Answers(models.Model):
    respondent = models.ForeignKey(Respondents, on_delete=models.CASCADE)
    sample_meta_data = models.ForeignKey(SampleMetaData, on_delete=models.CASCADE)
    naturalness = models.SmallIntegerField()
    intelligibility = models.SmallIntegerField()
