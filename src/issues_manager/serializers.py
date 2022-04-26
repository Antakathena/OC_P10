from rest_framework import serializers
from .models import Project, Issue, Comment, Contributors

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  ##
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author', 'owner'] ##


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class ContributorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = '__all__'

