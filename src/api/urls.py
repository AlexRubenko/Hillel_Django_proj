from django.urls import include, path
from rest_framework import routers

from api.views import (CADDocumentDetailView, CADDocumentViewList,
                       CustomerDelete, CustomerUpdate, CustomerViewSet,
                       ProjectDetailView, ProjectViewList)

app_name = "api"
router = routers.DefaultRouter()
router.register("customers", CustomerViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("customer_update/<int:pk>/", CustomerUpdate.as_view(), name="customer_update"),
    path("customer_delete/<int:pk>/", CustomerDelete.as_view(), name="customer_delete"),
    path("caddocuments/", CADDocumentViewList.as_view(), name="caddocuments_list"),
    path('caddocuments/<int:pk>/', CADDocumentDetailView.as_view(), name='cad-document-detail'),
    path("projects/", ProjectViewList.as_view(), name="projects_list"),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]
