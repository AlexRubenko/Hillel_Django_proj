from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from account.models import CustomUser


class Project(models.Model):
    name = models.CharField(max_length=100)
    project_number = models.CharField(max_length=25, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class CADDocument(models.Model):
    TYPE_CHOICES = (
        ('2D', '2D Drawing'),
        ('PDF', 'PDF Drawing'),
        ('3D', '3D Model File'),
        ('Spec', 'Specification'),
    )

    STATUS_CHOICES = (
        ('actual', 'Actual'),
        ('canceled', 'Canceled'),
    )
    document_number = models.CharField(max_length=50, blank=False, default="document number needed")
    document_name = models.CharField(max_length=100, blank=True, default="document name needed")
    document_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file = models.FileField(upload_to='media/cad_documents/', blank=True, null=True)
    description = models.TextField(max_length=300)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='actual')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False)
    uploaded = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents', to_field='project_number')

    class Meta:
        ordering = ['-uploaded']

    @property
    def file_url(self):
        if self.file:
            return self.file.url
        return None

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.file.name}"


class ChangeLog(models.Model):
    document = models.ForeignKey(CADDocument, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    change_datetime = models.DateTimeField(default=datetime.now)
    description = models.TextField()

    def __str__(self):
        return f"{self.document} - {self.change_datetime} by {self.user}"


@receiver(post_save, sender=CADDocument)
def create_change_log_on_document_creation(sender, instance, created, **kwargs):
    if created:
        ChangeLog.objects.create(
            document=instance,
            user=instance.uploaded_by,
            description=f"Document created on {instance.uploaded}"
        )


@receiver(post_save, sender=CADDocument)
def create_change_log_on_document_update(sender, instance, **kwargs):
    ChangeLog.objects.create(
        document=instance,
        user=instance.uploaded_by,
        description=f"Document updated on {instance.updated}"
    )


@receiver(post_delete, sender=CADDocument)
def create_change_log_on_document_deletion(sender, instance, **kwargs):
    ChangeLog.objects.create(
        document=instance,
        user=instance.uploaded_by,
        description=f"Document deleted on {instance.updated}"
    )
