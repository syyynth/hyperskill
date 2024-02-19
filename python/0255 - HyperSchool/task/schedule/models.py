from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    about = models.TextField()

    def __str__(self):
        return f'{self.name} {self.surname}'


class Course(models.Model):
    title = models.CharField(max_length=255)
    info = models.TextField()
    duration_months = models.IntegerField()
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    teacher = models.ManyToManyField(Teacher)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Student(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    age = models.IntegerField()
    course = models.ManyToManyField(Course)

    def __str__(self):
        return f'{self.name} {self.surname}'
