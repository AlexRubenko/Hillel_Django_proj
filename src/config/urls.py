from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('document_flow.urls')),
    path('document_flow/', include('document_flow.urls'))
]
