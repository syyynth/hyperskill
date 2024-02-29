from django.db import models


class Article(models.Model):
    text = models.TextField()
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f'{self.title}'
