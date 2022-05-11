from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from .models import Project, Issue, Comment, Contributor
from users.models import CustomUser


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    project_id = serializers.ReadOnlyField(source='id')
    
    class Meta:
        model = Project
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    issue_id = serializers.ReadOnlyField(source='id')
    
    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comment_id = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Comment
        fields = '__all__'


class ContributorsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contributor
        fields = '__all__'

