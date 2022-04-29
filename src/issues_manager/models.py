from django.db import models
from django.conf import settings
from django.db import models


class Project(models.Model):
    """author = author_user_id """
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_manager')

    def __str__(self):
        return f"{self.title}"


class Issue(models.Model):
    """
    Classe des problèmes liés à un projet (instance de Project).
    """
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    # project_id= models.IntegerField()
    project_id = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="projet_associe")
    status = models.CharField(max_length=128)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="auteur")  # créateur
    assignee_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="responsable")  # responsable
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (id:{self.id}), soulevé par {self.author_user_id}, responsable : {self.assignee_user_id}"


class Comment(models.Model):
    """
    Classe des commentaires liés à un problème (instance de Issue).
    """
    description = models.CharField(max_length=128)
    issue_id = models.ForeignKey(
        to=Issue, on_delete=models.CASCADE)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.headline}, écrit par {self.user}"


class Contributor(models.Model):
    """
    user_id = contributor,
    project_id = project(integerfield),
    permission(ChoiceField)
    role(Charfield)
    """
    CONTRIBUTEUR = 'contributeur'
    RESPONSABLE = 'responsable'
    CHOICES = [
        (CONTRIBUTEUR, "contributeur"),
        (RESPONSABLE, "responsable")
    ]

    contributor = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
        unique_together = ('contributor', 'project',)

    def __str__(self):
        return f"{self.contributor} participe au projet: {self.project}"
