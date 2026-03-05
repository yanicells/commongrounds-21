from django.urls import path
from .views import *

from . import views

app_name = 'commissions'

urlpatterns = [
<<<<<<< HEAD
    path('requests', views.RequestListView.as_view(), name='request-list'),
    path('request/<int:pk>', views.RequestDetailView.as_view(),
         name='request-detail'),
]
=======
    path('admin/', admin.site.urls),
    path('requests', CommissionListView.as_view(), name='list_view'),
    path('request/<int:pk>', CommissionDetailView.as_view(), name='detail_view')
]
>>>>>>> 9693708 (fix: urls and missing model field)
