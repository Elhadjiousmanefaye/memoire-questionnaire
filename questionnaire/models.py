from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User  # Import du modèle utilisateur
from django.contrib.auth.models import User

class Question(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)  # ✅ Lien avec l'utilisateur
    texte = models.TextField()
    reponse = models.TextField(blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auteur.username} - {self.texte[:50]}"


class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='etudiant')
    nom_complet = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    niveau = models.CharField(max_length=100, blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_complet
