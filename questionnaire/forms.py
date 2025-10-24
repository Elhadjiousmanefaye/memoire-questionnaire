from django import forms
from django.contrib.auth.models import User
from .models import Etudiant

class EtudiantInscriptionForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = Etudiant
        fields = ['nom_complet', 'email', 'niveau']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        etudiant = Etudiant(
            user=user,
            nom_complet=self.cleaned_data['nom_complet'],
            email=self.cleaned_data['email'],
            niveau=self.cleaned_data['niveau']
        )
        if commit:
            user.save()
            etudiant.save()
        return etudiant
