from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.views import (CADDocumentDetailView, CADDocumentViewList,
                       CustomerDelete, CustomerUpdate, CustomerViewSet,
                       ProjectDetailView, ProjectViewList)

app_name = "api"
router = routers.DefaultRouter()
router.register("customers", CustomerViewSet, basename="customers")


schema_view = get_schema_view(
    openapi.Info(
        title="Document_flow API",
        default_version="v1",
        description="API for organise document flow process",
        terms_of_service="https://www.goole.com/policies/terms/",
        contact=openapi.Contact(email='admin@admin.com'),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include(router.urls)),
    path("auth/", include("djoser.urls.jwt")),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="swagger_docs"),
    path("customer_update/<int:pk>/", CustomerUpdate.as_view(), name="customer_update"),
    path("customer_delete/<int:pk>/", CustomerDelete.as_view(), name="customer_delete"),
    path("caddocuments/", CADDocumentViewList.as_view(), name="caddocuments_list"),
    path('caddocuments/<int:pk>/', CADDocumentDetailView.as_view(), name='cad-document-detail'),
    path("projects/", ProjectViewList.as_view(), name="projects_list"),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]

