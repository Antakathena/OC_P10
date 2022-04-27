from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor

class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  ##
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author'] ##


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'


class ContributorsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contributor
        fields = '__all__'

