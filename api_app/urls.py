from django.urls import path
from .views import ApiQrCode

urlpatterns = [
    path('qrcode/', ApiQrCode.as_view())
]