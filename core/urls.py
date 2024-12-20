from django.urls import path
from core.getuserGroup import UserGroupAPIView
 
urlpatterns = [
    path('get-user-group/', UserGroupAPIView.as_view(), name='user-group'),
]
