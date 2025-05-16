from django.urls import path
from .views import test_api, save_script,upload_folder,cleanup_inactive_batches,delete_batch


urlpatterns = [
    path('test/', test_api),
    path('save-script/', save_script),
    path('upload-folder/', upload_folder),
    path('cleanup-inactive-batches/', cleanup_inactive_batches),
    path('delete-batch/<str:batch_id>/', delete_batch),


]
