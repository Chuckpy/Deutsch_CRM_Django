from django.db import models
from quizes.models import Quiz


class Questao(models.Model):
    texto = models.CharField(max_length=220)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.texto)

    def get_answers(self):
        return self.respostas.all()        

    class Meta :
        verbose_name = "Questão"
        verbose_name_plural = "Questões"


class Resposta(models.Model):
    texto = models.CharField(max_length=220)
    correto = models.BooleanField(default=False)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name="respostas")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"questao:{self.questao.texto}, respostas : {self.texto},correct:{self.correto}"
