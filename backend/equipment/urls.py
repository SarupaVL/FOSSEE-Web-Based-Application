from django.urls import path
from .views import test_api, upload_csv, upload_history, generate_report

urlpatterns = [
    path('test/', test_api),
    path('upload/', upload_csv),
    path('history/', upload_history),
    path('report/<int:upload_id>/', generate_report),
]
