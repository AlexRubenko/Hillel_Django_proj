from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import (CADDocumentSerializer, CustomerSerializer,
                             ProjectSerializer)
from document_flow.models import CADDocument, Project


class CustomerViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


class CustomerUpdate(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


class CustomerDelete(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


class CADDocumentViewList(ListAPIView):
    queryset = CADDocument.objects.all()
    serializer_class = CADDocumentSerializer


class CADDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CADDocument.objects.all()
    serializer_class = CADDocumentSerializer


class ProjectViewList(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
