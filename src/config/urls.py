from django.contrib import admin
from django.urls import include, path

from document_flow.views import index

handler404 = 'document_flow.views.custom_404_view'


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name='index'),
    path('api-auth/', include('rest_framework.urls')),
    path("api/", include('api.urls')),
    path('document_flow/', include('document_flow.urls'))
]
