from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, AccountView, UpdateTokenView

app_name = 'authentication'
urlpatterns = [
    path('auth/signup', RegistrationAPIView.as_view()),
    path('auth/signin', LoginAPIView.as_view()),
    path('view', AccountView.as_view()),
    path('auth/update', UpdateTokenView.as_view()),
]