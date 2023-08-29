from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from account.models import CustomUser


class ChangeLog(models.Model):
    document = models.ForeignKey('CADDocument', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    change_datetime = models.DateTimeField(default=datetime.now)
    description = models.TextField()

    def __str__(self):
        return f"{self.document} - {self.change_datetime} by {self.user}"


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

    document_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file = models.FileField(upload_to='media/cad_documents/', blank=True, null=True)
    description = models.TextField(max_length=300)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='actual')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False)
    uploaded = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded']

    @property
    def file_url(self):
        if self.file:
            return self.file.url
        return None

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.file.name}"


class Project(models.Model):
    name = models.CharField(max_length=100)
    project_number = models.CharField(max_length=25)
    documents = models.ManyToManyField(CADDocument, blank=True, related_name="projects")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


@receiver(post_save, sender=CADDocument)
def create_document_update_log(sender, instance, created, **kwargs):
    user = CustomUser.objects.first()
    if not created:
        ChangeLog.objects.create(
            document=instance,
            user=user,
            description=f"Document {instance.id} was updated."
        )


@receiver(post_delete, sender=CADDocument)
def create_document_delete_log(sender, instance, **kwargs):
    user = CustomUser.objects.first()
    ChangeLog.objects.create(
        document=instance,
        user=user,
        description=f"Document {instance.id} was deleted."
    )
