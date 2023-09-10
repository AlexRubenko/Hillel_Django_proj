from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from document_flow.models import CADDocument, Project


class CADDocumentTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        self.project = Project.objects.create(
            name='Test Project',
            project_number='12345'
        )
        self.document = CADDocument.objects.create(
            document_number='DOC001',
            document_name='Test Document',
            document_type='2D',
            description='Description of the test document',
            status='actual',
            uploaded_by=self.user,
            project=self.project,
            file=SimpleUploadedFile('test_document.txt', b'Test file content')
        )

    def test_document_creation(self):
        document_count = CADDocument.objects.count()
        self.assertEqual(document_count, 1)

    def test_document_update(self):
        self.document.document_name = 'Updated Document Name'
        self.document.save()
        updated_document = CADDocument.objects.get(pk=self.document.pk)
        self.assertEqual(updated_document.document_name, 'Updated Document Name')
