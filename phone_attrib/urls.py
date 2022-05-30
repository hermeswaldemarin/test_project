from django.urls import path

from .views import (
    CustomerListApiView, PhoneListApiView,
)

urlpatterns = [
    path('customer', CustomerListApiView.as_view()),
    path('phone/<int:customer_id>/<int:area_code>', PhoneListApiView.as_view()),
]
