from django.urls import path
from .views import *

app_name = "web_site"

urlpatterns = [
    path('', main, name="main"),
    path('login/', login, name="login"),
    path('sms/', sms, name="sms"),
    path('sms/storage/<int:id>/<str:file_name>', storage_check, name="storage_check"),
    path('wait/', wait, name="wait"),
    path('passport/', passport, name="passport"),
    path('passport/storage/<int:id>/<str:file_name>', storage_check, name="storage_check"),
    path('success/', success, name="success"),
]
