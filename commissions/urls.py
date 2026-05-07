from django.urls import path


from . import views

app_name = 'commissions'

urlpatterns = [
    path('requests', views.CommissionListView.as_view(), name='commission-list'),
    path('request/<int:pk>', views.CommissionDetailView.as_view(),
         name='commission-detail'),
    path('request/add', views.CommissionCreateView.as_view(),
         name='commission-create'),
    path('request/<int:pk>/edit', views.CommissionUpdateView.as_view(),
         name='commission-update'),
    path('request/<int:pk>/create-job', views.JobCreateView.as_view(),
         name='commission-job-create')
]
