from django.contrib.auth.models import User
from django.db import models


class QuestionManager(models.Manager):
    def new(self):
        pass

    def popular(self):
        pass


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    likes = models.ManyToManyField(User, related_name="likes")

    objects = QuestionManager()


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateField()
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
