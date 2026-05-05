from django.urls import path

from . import views

app_name = 'diyprojects'

urlpatterns = [
    path('projects', views.ProjectListView.as_view(), name='project-list'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(),
         name='project-detail'),
    path('project/add', views.ProjectCreateView.as_view(), name='project-add'),
    path('project/<int:pk>/edit', views.project_update_view, name='item-update')
]
