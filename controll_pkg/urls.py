from django.urls import path
from controll_pkg.views import ProjectsView, FlyView, ObjectsView,\
                               ProjectsCreateView, FlyCreateView,\
                               ObjectsCreateView, ProjectDeleteView,\
                               FlyDeleteView, ObjectsDeleteView,\
                               ObservationObjectChronologyDeleteView

app_name = 'authentication'
urlpatterns = [
    path('project/get', ProjectsView.as_view()),
    path('project/create', ProjectsCreateView.as_view()),
    path('project/delete', ProjectDeleteView.as_view()),
    
    path('fly/get', FlyView.as_view()),
    path('fly/create', FlyCreateView.as_view()),
    path('fly/delete', FlyDeleteView.as_view()),
    
    path('object/get', ObjectsView.as_view()),
    path('object/create', ObjectsCreateView.as_view()),
    path('object/delete', ObjectsDeleteView.as_view()),
    
    path('objects/delete', ObservationObjectChronologyDeleteView.as_view())
]