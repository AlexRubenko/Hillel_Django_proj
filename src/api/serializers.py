from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from document_flow.models import CADDocument, Project


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "is_staff", "role", "phone_number", "is_active", "access_status")


class CADDocumentSerializer(ModelSerializer):
    class Meta:
        model = CADDocument
        fields = ("document_number", "document_name", "project", "status")


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ("name", "project_number", "created")
