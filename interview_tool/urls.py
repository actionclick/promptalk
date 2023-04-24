from django.urls import path
from . import views

app_name = 'interview'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('start/', views.start_interview, name='start'),
]

