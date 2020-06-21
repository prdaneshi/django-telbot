from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=50, null=True)
    birth = models.PositiveIntegerField(null=True)
    city = models.CharField(max_length=50, null=True)
    gender = models.BooleanField(null=True)
    chatId = models.IntegerField(null=True)
    last_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name
