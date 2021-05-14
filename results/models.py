from django.db import models
from quizes.models import Quiz
from users.models import User

class Resultado(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resultado = models.FloatField()

    def __str__(self):
        return str(self.pk)