from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from .models import Project, Issue, Comment, Contributor
from users.models import CustomUser


class ProjectSerializer(serializers.ModelSerializer):
    # class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'type',
            'author',
            ] 


class IssueSerializer(serializers.ModelSerializer):
    # class IssueSerializer(serializers.NestedHyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    issue_id = serializers.ReadOnlyField(source='id')
    # project = serializers.PrimaryKeyRelatedField(many=False, queryset=Project.objects.filter(id=...))

    # project = serializers.RelatedField(read_only=True)

    # assignee = serializers.SlugRelatedField( # plutôt que ReadOnly?
    #     queryset=CustomUser.objects.all(),
    #     slug_field='username',
    #     default=serializers.CurrentUserDefault()
    # )
    
    # parent_lookup_kwargs = {
    #     'project_id': 'project__id',
    # }
    class Meta:
        model = Issue
        fields = '__all__'
        
        #  [
        #     'title',
        #     'description',
        #     'tag',
        #     'priority',
        #     'project',
        #     'status',
        #     'author',
        #     'issue_id',
        #     'assignee',
        #     'created_time',
        #     ]

    # def validate_assignee(self, assignee, project):
    #      print("self:")
    #      print(self)
    #      print("assignee:" + str(assignee))
    #      user_id = assignee.id
    #      print("user_id:"+ str(user_id))
    #      print(self.project)
    # #     # print (Contributor.objects.all())
    # #     # if not Contributor.objects.filter(
    # #     #     user=user_id, project= self.project).exists():
    # #     #     error_message = str(assignee) +"n'est pas collaborateur du projet"
    # #     #     raise serializers.validationError(error_message)
    #      return assignee
    


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

