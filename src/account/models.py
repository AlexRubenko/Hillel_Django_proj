from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from account.managers import CustomerManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ACCESS_CHOICES = (
        ('edit', 'Full Edit Access'),
        ('view', 'View-Only Access'),
    )

    ROLES = (
        ('manager', 'Manager'),
        ('engineer', 'Engineer'),
    )

    role = models.CharField(max_length=20, choices=ROLES)
    first_name = models.CharField(_("Name"), max_length=150)
    last_name = models.CharField(_("Surname"), max_length=150)
    email = models.EmailField(_("Email address"), unique=True, blank=False, null=False)
    phone_number = PhoneNumberField(_("Phone number"), null=True, blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    access_status = models.CharField(max_length=20, choices=ACCESS_CHOICES, default='view')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomerManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
