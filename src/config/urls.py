from django.contrib import admin
from django.urls import include, path

import document_flow
from document_flow.urls import index

handler404 = 'document_flow.views.custom_404_view'


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('document_flow.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path("api/", include('api.urls')),
    path('document_flow/', include('document_flow.urls'))
]
