from django.urls import path
from document_flow.views import index, get_documents, update_document, delete_document

urlpatterns = [
    path('', index, name='index'),
    path("get_documents", get_documents, name="get_documents"),
    path("update/<pk>/", update_document, name="update_student"),
    path("delete/<pk>/", delete_document, name="delete_document")
]
