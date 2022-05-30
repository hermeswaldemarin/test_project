from django.urls import path, include
from .views import (
    CustomerListApiView, PhoneListApiView,
)

urlpatterns = [
    path('customer', CustomerListApiView.as_view()),
    path('phone/<int:customerId>/<int:areaCode>', PhoneListApiView.as_view()),
]