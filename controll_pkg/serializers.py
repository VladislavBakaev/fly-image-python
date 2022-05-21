from rest_framework import serializers
from controll_pkg.models import Project
from authentication.serializers import AccountSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields = ('name', 'at_create', 'at_update', 'author')


class ProjectCreateSerializator(serializers.Serializer):
    name = serializers.CharField()
    
    class Meta:
        fields=['name']
        

class FlyCreateSerializator(serializers.Serializer):
    
    class Meta:
        fields=[]