from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE
    )

    text = models.CharField(max_length=255)

    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)

    correct_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.text


class RecommendationPackage(models.Model):

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    def __str__(self):
        return self.title