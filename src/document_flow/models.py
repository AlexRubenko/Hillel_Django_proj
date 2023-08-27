from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import datetime


class CustomUser(models.Model):
    ACCESS_CHOICES = (
        ('edit', 'Full Edit Access'),
        ('view', 'View-Only Access'),
    )

    ROLES = (
        ('manager', 'Manager'),
        ('engineer', 'Engineer'),
    )

    role = models.CharField(max_length=20, choices=ROLES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=False)
    access_status = models.CharField(max_length=20, choices=ACCESS_CHOICES, default='view')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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
    file = models.FileField(upload_to='cad_documents/')
    description = models.TextField(max_length=300)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='actual')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.file.name}"


class Project(models.Model):
    name = models.CharField(max_length=100)
    project_number = models.CharField(max_length=25)
    documents = models.ManyToManyField(CADDocument, blank=True, related_name="projects")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=CADDocument)
def create_document_update_log(sender, instance, created, **kwargs):
    user = CustomUser.objects.first()  # Это временное решение
    if not created:
        ChangeLog.objects.create(
            document=instance,
            user=user,
            description=f"Document {instance.id} was updated."
        )


@receiver(post_delete, sender=CADDocument)
def create_document_delete_log(sender, instance, **kwargs):
    user = CustomUser.objects.first()  # Это временное решение
    ChangeLog.objects.create(
        document=instance,
        user=user,
        description=f"Document {instance.id} was deleted."
    )
