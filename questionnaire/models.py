from django.db import models

# Create your models here.

from django.db import models

class Question(models.Model):
    texte = models.TextField()
    reponse = models.TextField(blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texte[:80]
