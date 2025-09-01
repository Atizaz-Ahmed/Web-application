from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    options = models.JSONField()
    correct_option = models.CharField(max_length=100)

    def __str__(self):
        return self.question_text

class login_info(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    has_taken_quiz = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Results(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    result = models.IntegerField()

    def __str__(self):
        return f"{self.username}: {self.result}"
