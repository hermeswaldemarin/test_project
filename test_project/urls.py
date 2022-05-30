from django.contrib import admin
from django.urls import path, include
from phone_attrib import urls as phone_attrib_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('phone-attrib/', include(phone_attrib_urls)),
]
