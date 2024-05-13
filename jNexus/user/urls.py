from django.urls import path
from user.views import GoogleView


urlpatterns = [
 
    path('google-auth/', GoogleView.as_view(), name='google'),

]