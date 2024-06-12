from django.urls import path
from .views import *

urlpatterns = [
    path('filteruser/', UserListView.as_view(), name="filteruser"),
    path('getmesseges/', MessegeView.as_view(), name="getmesseges"),
    path('createmesseges/', CreateMessegeView.as_view(), name="createmesseges"),
    path('updateprofile/', UpdateUserProfileView.as_view(), name="updateprofile"),
]