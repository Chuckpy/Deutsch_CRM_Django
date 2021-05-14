from django.db import models
from model_utils.models import TimeStampedModel
from autoslug import AutoSlugField
from django.urls import reverse
import random

Escolhas= (
        ("Fácil", "Fácil"),
        ("Médio", "Médio"),
        ("Dificil", "Dificil"),
)


class Categoria(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(unique=True, always_update=False, populate_from="name")

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("quiz:list_by_category", kwargs={"slug": self.slug})



class Quiz(models.Model) :
    nome = models.CharField(max_length=100)
    topico =  models.CharField(max_length=100)
    numero_questoes = models.IntegerField()
    tempo = models.IntegerField(help_text="duração em minutos do quiz")
    porcentagem_necessaria = models.IntegerField(help_text="Porcentagem necessária para passar",
     default = 0, blank=True, null=True)
    dificuldade = models.CharField(choices=Escolhas, max_length=250)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True, help_text="Pode ser nula")

    def __str__(self):
        return f"{self.nome} - {self.topico}"
    
    def get_questions(self):
        questions = list(self.questao_set.all())
        random.shuffle(questions)
        return questions[:self.numero_questoes]

    class Meta:
        verbose_name_plural = "Quizes"


