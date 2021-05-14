from users.models import User
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from PIL import Image
from django.db import models
from ckeditor.fields import RichTextField



class Category(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(unique=True, always_update=False, populate_from="name")
    class Meta:
        ordering = ("name",)
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:list_by_category", kwargs={"slug": self.slug})


class Post(models.Model):
    title = models.CharField("Titulo" ,max_length=100)
    slug = AutoSlugField(unique=True, always_update=False, populate_from="title")
    author = models.ForeignKey(User,related_name="autor", on_delete=models.CASCADE)
    body = RichTextField("Texto",max_length=2050, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True, upload_to='blog/images')
    favorite = models.ManyToManyField(User, default=None, blank=True, related_name="favorito")   
    category = models.ManyToManyField(Category,blank=True)

    class Meta:
        ordering = ("-created",)
        verbose_name_plural = "Noticias"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    def comment_number(self):
        return len(self.comment_set.all())

    @property
    def favorite_number(self):
        return self.favorite.all().count()

    # redimensionando imagem para um maximo de 1300x1300 px
    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 1300 or img.width >1300 :
            output_size = (1300, 1300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Comentários"


FAVORITE_CHOICES = (
    ("Favoritar","Favoritar"),
    ("Desfavoritar","Desfavoritar")
)
class Favorite(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="favoritado")   
    value = models.CharField(choices=FAVORITE_CHOICES, default="Favoritar", max_length=15)
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    class Meta :
        verbose_name_plural = "Favoritos"
        constraints = (models.UniqueConstraint(fields=['author_id', 'post_id'], name='unique_favorite'),)
        def __str__(self):
            return str(self.post)
