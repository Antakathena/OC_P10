from django.db import models
from django.conf import settings
from django.db import models


class Project(models.Model):
    """
    Modèle des projets
    """

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_manager')

    def __str__(self):
        return f"{self.title}"


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
        return f"Problème (id:{self.id}) : {self.title} , soulevé par {self.author}, responsable : {self.assignee}"


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
        return f"Commentaire {self.id}, écrit par {self.author}"


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
        return f"{self.user} participe au projet: {self.project}, en tant que {self.permission}"
