from django.db import models


class Record(models.Model):
    regex = models.CharField(max_length=50)
    text = models.CharField(max_length=1024)
    result = models.BooleanField()

    def __str__(self):
        return f'regex: {self.regex}, text: {self.text}, result: {self.result}'
