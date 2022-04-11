from rest_framework import serializers
from .models import Project, Issue, Comment, Contributors

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'manager', 'contributors']


