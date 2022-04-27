from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from .models import Project, Issue, Comment, Contributor

class ProjectSerializer(serializers.ModelSerializer):
# class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    issues = serializers.ReadOnlyField(source='self.issues')
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author', 'issues'] # issues ajouté
    
class IssueSerializer(serializers.ModelSerializer):
# class IssueSerializer(serializers.NestedHyperlinkedModelSerializer):   
    author = serializers.ReadOnlyField(source='author.username')
    
    # parent_lookup_kwargs = {
    #     'project_id': 'project__id',
    # }
    class Meta:
        model = Issue
        fields = ['title', 'description', 'tag', 'priority', 'project_id', 'status', 'author_user_id','assignee_user_id', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
# class CommentSerializer(serializers.NestedHyperlinkedModelSerializer): 
    author = serializers.ReadOnlyField(source='author.username')

    # parent_lookup_kwargs = {
    #     'issue_id': 'issue__id',
    #     'project_id': 'project__id',
    # }

    class Meta:
        model = Comment
        fields = '__all__'


class ContributorsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contributor
        fields = '__all__'

