from django.db import models
from django.conf import settings
from django.db import models

import users


class Project(models.Model):
    """
    Modèle des projets
    """

    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_manager')

    def save(self, *args, **kwargs):
        # à ce moment le project_id n'existe pas
        old_project_id = self.id
        # puis on le créé avec le super().save
        super().save(*args, **kwargs)
        if old_project_id is None:
            Contributor.objects.create(user=self.author,project=self,role='auteur')

    def __str__(self):
        return f"{self.title}(projet {self.id})"


class Issue(models.Model):
    """
    Modèle des problèmes liés à une instance de Projet.
    """

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="issue")
    status = models.CharField(max_length=128)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="auteur")  # créateur
    assignee = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="responsable")  # responsable
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project}, (issue {self.id})   {self.title} , {self.status}, responsable : {self.assignee}"


class Comment(models.Model):
    """
    Modèle des commentaires liés à un problème (instance de Issue).
    """
    description = models.CharField(max_length=128)
    issue = models.ForeignKey(
        to=Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"(Commentaire {self.id}) {self.description} écrit par {self.author}, {self.issue}"


class Contributor(models.Model):
    """
    Modèle pour associer des utilisateurs à un projet en tant que contributeurs.
    """

    # il faudrait rendre le message d'erreur  "Les champs user,
    # project doivent former un ensemble unique." plus clair ""

    CONTRIBUTEUR = 'contributeur'
    RESPONSABLE = 'responsable'
    CHOICES = [
        (CONTRIBUTEUR, "contributeur"),
        (RESPONSABLE, "responsable")
    ]

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    permission = models.CharField(
        max_length=15,
        choices=CHOICES,
        default=CONTRIBUTEUR,
    )
    role = models.CharField(max_length=128)

    class Meta:
        # ensures we don't get multiple instances
        # for unique user-project pairs
        unique_together = ('user', 'project', )

    def __str__(self):
        return f"{self.user}, {self.project}"
