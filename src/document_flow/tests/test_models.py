from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from document_flow.models import CADDocument, ChangeLog, Project

User = get_user_model()


class CADDocumentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpass')
        self.document = CADDocument.objects.create(
            document_type='2D',
            description='Test document',
            status='actual',
            uploaded_by=self.user
        )

    def test_document_str(self):
        self.assertEqual(str(self.document), f"2D Drawing - {self.document.file.name}")

    def test_document_file_url(self):
        self.assertIsNone(self.document.file_url)


class ChangeLogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpass')
        self.document = CADDocument.objects.create(
            document_type='2D',
            description='Test document',
            status='actual',
            uploaded_by=self.user
        )
        self.log = ChangeLog.objects.create(
            document=self.document,
            user=self.user,
            change_datetime=datetime.now(),
            description='Test description'
        )

    def test_log_str(self):
        self.assertEqual(str(self.log), f"{self.document} - {self.log.change_datetime} by {self.log.user}")


class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpass')
        self.document = CADDocument.objects.create(
            document_type='2D',
            description='Test document',
            status='actual',
            uploaded_by=self.user
        )
        self.project = Project.objects.create(
            name='Test Project',
            project_number='123',
        )
        self.project.documents.add(self.document)

    def test_project_str(self):
        self.assertEqual(str(self.project), self.project.name)

    def test_project_documents(self):
        self.assertIn(self.document, self.project.documents.all())
