from django.urls import path

from . import views

app_name = 'diyprojects'

urlpatterns = [
    path('projects', views.ProjectListView.as_view(), name='project-list'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(),
         name='project-detail'),
]
