from django.urls import path
from .views import test_api, upload_csv, upload_history

urlpatterns = [
    path('test/', test_api),
    path('upload/', upload_csv),
    path('history/', upload_history),
]
