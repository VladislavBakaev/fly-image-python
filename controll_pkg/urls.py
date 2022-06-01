from django.urls import path
from controll_pkg.views import ProjectsView, FlyView, ObjectsView,\
                               ProjectsCreateView, FlyCreateView,\
                               ObjectsCreateView, ProjectDeleteView

app_name = 'authentication'
urlpatterns = [
    path('project/get', ProjectsView.as_view()),
    path('project/create', ProjectsCreateView.as_view()),
    path('project/delete', ProjectDeleteView.as_view()),
    
    path('fly/get', FlyView.as_view()),
    path('fly/create', FlyCreateView.as_view()),
    
    path('object/get', ObjectsView.as_view()),
    path('object/create', ObjectsCreateView.as_view())
]