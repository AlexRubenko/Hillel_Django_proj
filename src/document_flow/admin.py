from django.contrib import admin

from document_flow.models import CADDocument, Project

admin.site.register([CADDocument, Project])
