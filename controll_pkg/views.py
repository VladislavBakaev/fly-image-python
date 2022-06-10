from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from django.db import IntegrityError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import FileUploadParser, JSONParser
from datetime import datetime

import json
from controll_pkg.models import Project, Fly, ObservationObjectChronology, FlyImage, ObservationObject
from controll_pkg.serializers import ProjectCreateSerializator
from authentication.models import Account

class ProjectsView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request):
        target_id = request.query_params.get('id', None)
        if (target_id):
            projects_qs = Project.objects.filter(id=target_id)
        else:
            projects_qs = Project.objects.all()
            
        projects = json.loads(serializers.serialize('json', projects_qs))
        for i, project in enumerate(projects):
            project.pop('model')
            project.update(project.pop('fields'))
            
            project['fly_count'] = Fly.objects.filter(project__id=project['pk']).count()
            project['object_count'] = ObservationObjectChronology.objects.filter(project__id=project['pk']).count()
            project['author'] = projects_qs[i].author.name
            project['id']=project.pop('pk')

        return Response(projects, status=status.HTTP_200_OK)
    
class ProjectsCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectCreateSerializator

    def post(self, request):
        account = Account.objects.get(user=request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            new_project = Project.objects.create(
                name=serializer.data['name'],
                author=account,
                at_create=datetime.now(),
                at_update=datetime.now()
            )
        except IntegrityError as e:
            return Response({'errors':['Название проекта должно быть уникальным']},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'id':new_project.pk}, status.HTTP_201_CREATED)

class ProjectDeleteView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def delete(self, request):
        account = Account.objects.get(user=request.user)
        try:
            project = Project.objects.get(id = request.data.get('id'))
        except:
            return Response({'error':'invalid id: {0}'.format(request.data.get('id'))}, status=status.HTTP_400_BAD_REQUEST)

        if project.author == account:
            project.delete()
        else:
            return Response({'error':'forbiden'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        return Response({}, status.HTTP_200_OK)

    
class FlyView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request):
        target_id = request.query_params.get('project_id', None)

        if (target_id):
            flying_qs = Fly.objects.filter(project__id=target_id)
        else:
            flying_qs = Fly.objects.all()
        flying = json.loads(serializers.serialize('json', flying_qs))

        for i, fly in enumerate(flying):
            fly.pop('model')
            fly['id']=fly.pop('pk')
            fly.update(fly.pop('fields'))
            fly['author'] = flying_qs[i].author.name
            
            photos_qs = FlyImage.objects.filter(fly__id=fly['id'])
            photos = json.loads(serializers.serialize('json', photos_qs))
            fly['photos'] = []
            for photo in photos:
                photo['fields'].pop('fly')
                photo['fields']['coordinate'] = list(map(float, photo['fields']['coordinate'].split(';')))
                photo['fields']['id'] = photo['pk']
                photo['fields']['name'] = photo['fields']['image'].split('/')[1]
                fly['photos'].append(photo['fields'])
        
        return Response(flying, status=status.HTTP_200_OK)

class FlyCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_class = [JSONParser, FileUploadParser]
    
    def post(self, request):
        account = Account.objects.get(user=request.user)
        files = request.FILES
        data = json.loads(request.data['fly'])
        
        date = datetime.strptime(data.get('date').split('.')[0],"%Y-%m-%dT%H:%M:%S")
        
        new_fly = Fly(author=account)
        new_fly.at_create = datetime.now()
        new_fly.at_fly = date
        new_fly.project_id = data.get('project')
        new_fly.name = data.get('name')
        new_fly.robot_type = data.get('robot', None)
        new_fly.camera_type = data.get('camera', None)
        new_fly.commentary = data.get('commentary', None)
        new_fly.images_coords = json.dumps(data.get('coords', []))
        new_fly.save()
        
        for image_name in files:
            new_image = FlyImage()
            new_image.fly = new_fly
            new_image.coordinate = image_name
            new_image.image = files[image_name]
            new_image.save()
            
        
        return Response({}, status=status.HTTP_201_CREATED)

    def put(self, request):
        files = request.FILES
        data = json.loads(request.data['fly'])
        
        target_fly = Fly.objects.get(id=data['fly'])
        if(data.get('name', None)):
            target_fly.name = data.get('name')   
        if(data.get('robot', None)):
            target_fly.robot_type = data.get('robot')   
        if(data.get('camera', None)):
            target_fly.camera_type = data.get('camera')   
        if(data.get('commentary', None)):
            target_fly.commentary = data.get('commentary')
        if(data.get('date', None)):
            target_fly.at_fly = datetime.strptime(data.get('date').split('.')[0],"%Y-%m-%dT%H:%M:%S")
        
        target_fly.save()
        
        for image_name in files:
            new_image = FlyImage()
            new_image.fly = target_fly
            new_image.coordinate = image_name
            new_image.image = files[image_name]
            new_image.save()
        
        
        return Response({}, status=status.HTTP_201_CREATED)

class ObjectsView(APIView):
    def get(self, request):
        target_id = request.query_params.get('project_id', None)

        if (target_id):
            objects_chrns_qs = ObservationObjectChronology.objects.filter(project__id=target_id)
        else:
            objects_chrns_qs = ObservationObjectChronology.objects.all()
        
        objects_chrns = json.loads(serializers.serialize('json', objects_chrns_qs))
        for (i, objects_chrn) in enumerate(objects_chrns):
            objects_chrn.pop('model')
            objects_chrn['id']=objects_chrn.pop('pk')
            objects_chrn.update(objects_chrn.pop('fields'))
            objects_chrn['author'] = objects_chrns_qs[i].author.name
            objects_chrn['coordinate'] = list(map(float, objects_chrn['coordinate'].split(';')))
            
            chronology_qs = ObservationObject.objects.filter(chronology__id=objects_chrn['id'])
            chronology = json.loads(serializers.serialize('json', chronology_qs))
            objects_chrn['objects'] = []
            for (i, object) in enumerate(chronology):
                object.pop('model')
                object['id']=object.pop('pk')
                object.update(object.pop('fields'))
                object['image_box'] = json.loads(object['image_box'])
                object['author'] = chronology_qs[i].author.name
                object['image'] = str(chronology_qs[i].image.image)
                objects_chrn['objects'].append(object)
                
        return Response(objects_chrns, status=status.HTTP_200_OK)
    

class ObjectsCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_class = [JSONParser]
    
    def post(self, request):
        account = Account.objects.get(user=request.user)
        data = request.data
        
        if data.get('target_id', None):
            chronology = ObservationObjectChronology.objects.get(id=data.get('target_id', None))
        else:
            chronology = ObservationObjectChronology(
                name=data.get('name', None),
                author=account,
                at_create=datetime.now(),
                at_update=datetime.now(),
                project_id=data.get('project_id'),
                coordinate=data.get('coordinate'),
                commentary=data.get('commentary')
            )
            chronology.save()
            
        new_object = ObservationObject()
        chronology.at_update = datetime.now()
        new_object.chronology = chronology
        new_object.author = account
        new_object.at_create = datetime.now()
        new_object.image = FlyImage.objects.get(id=data.get('photo_id'))
        new_object.image_box = json.dumps(data.get('rect'))
        new_object.save()
        
        return Response({}, status=status.HTTP_201_CREATED)