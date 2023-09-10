from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from account.models import CustomUser
from document_flow.models import CADDocument, Project


class CADDocumentForm(forms.ModelForm):
    class Meta:
        model = CADDocument
        fields = '__all__'

    uploaded_by = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        empty_label=None,
        required=True,
    )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autofocus': True}),
    )
