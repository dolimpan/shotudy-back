from django.urls import path
from .views.ocr_views import test_api
from .views.ocr_views import ocr_function

urlpatterns = [
    path('test/', test_api),
    path('ocr/', ocr_function)
]