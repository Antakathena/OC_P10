from django.test import TestCase

# Create your tests here.
from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from .models import Project

class TestProject(APITestCase):
    # Nous stockons l’url de l'endpoint dans un attribut de classe
    # pour pouvoir l’utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('/issues_manager/projects')

    def format_datetime(self, value):
        # Cette méthode est un helper permettant de formater une date en chaine de caractères sous le même format que celui de l’api
        # si on ajoute un 
        #'date_created': self.format_datetime(project.date_created),
        # ou un
        #'date_updated': self.format_datetime(project.date_updated),
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def test_list(self):
        # Créons deux catégories dont une seule est active
        project = Project.objects.create(name='Projet X', active=True)
        Project.objects.create(name='Projet Z', active=False)

        # On réalise l’appel en GET en utilisant le client de la classe de test
        response = self.client.get(self.url)
        # Nous vérifions que le status code est bien 200
        # et que les valeurs retournées sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': project.pk,
                'title': project.title,
                'description': project.type,
                'author': project.author,
            }
        ]
        self.assertEqual(excepted, response.json())

    def test_create(self):
        # Nous vérifions qu’aucun projet n'existe avant de tenter d’en créer un
        self.assertFalse(Project.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouveau Projet'})
        # Vérifions que le status code est bien en erreur et nous empêche de créer un objet
        self.assertEqual(response.status_code, 405)
        # Enfin, vérifions qu'aucune nouvelle catégorie n’a été créée malgré le status code 405
        self.assertFalse(Project.objects.exists())