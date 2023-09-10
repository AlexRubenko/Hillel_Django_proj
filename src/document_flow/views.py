from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from webargs import fields
from webargs.djangoparser import use_args

from account.models import CustomUser
from document_flow.forms import (CADDocumentForm, EmailAuthenticationForm,
                                 ProjectForm)
from document_flow.models import CADDocument, Project


def index(request):
    return render(request, 'document_flow/index.html')


class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('get_documents')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password. Please try again.')
        return super().form_invalid(form)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'role', 'access_status')


def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/create_user.html', {'form': form})


def user_detail(request, id):
    user = get_object_or_404(get_user_model(), id=id)
    return render(request, 'registration/user_detail.html', {'user': user})


def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'registration/user_list.html', {'users': users})


def update_user(request, id):
    user = get_object_or_404(get_user_model(), id=id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_detail', id=user.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, 'registration/update_user.html', {'form': form, 'user': user})


def delete_user(request, id):
    user = get_object_or_404(get_user_model(), id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('user_list')
    return render(request, 'registration/delete_user.html', {'user': user})


class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('projects_list')
    else:
        form = ProjectForm()

    return render(request, 'document_flow/create_project.html', {'form': form})


def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'document_flow/projects_list.html', {'projects': projects})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'document_flow/project_detail.html', {'project': project})


def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('projects_list')

    return render(request, 'document_flow/delete_project.html', {'project': project})


@use_args(
    {
        "document_number": fields.Str(
            required=False,
        ),
        "document_name": fields.Str(
            required=False,
        ),
        "search": fields.Str(
            required=False,
        ),
    },
    location="query"
)
def get_documents(request, params):
    print(params)
    documents = CADDocument.objects.all()

    search_fields = ["document_number", "document_name"]

    for param_name, param_value in params.items():
        if param_name == "search":
            or_filter = Q()
            for field in search_fields:
                or_filter |= Q(**{F"{field}__icontains": param_value})
            documents = documents.filter(or_filter)
        else:
            documents = documents.filter(**{param_name: param_value})

    return render(request,
                  template_name="document_flow/documents_list.html",
                  context={"documents": documents})


@login_required
@csrf_exempt
def create_document(request):
    if request.method == 'POST':
        form = CADDocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            return redirect('document_flow:get_documents')
    else:
        form = CADDocumentForm()

    return render(request, 'document_flow/create_document.html', {'form': form})


@login_required
@csrf_exempt
def update_document(request, pk):
    document = get_object_or_404(CADDocument, pk=pk)

    if request.method == 'POST':
        form = CADDocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_flow:get_documents')
    else:
        form = CADDocumentForm(instance=document)

    return render(request, 'document_flow/update_document.html', {'form': form, 'document': document})


@login_required
@csrf_exempt
def delete_document(request, pk):
    document = get_object_or_404(CADDocument, pk=pk)

    if request.method == 'POST':
        document.delete()
        return redirect('get_documents')

    return render(request, 'document_flow/delete_document.html', {'document': document})


def custom_404_view(request, exception):
    context = {
        'error_message': 'Sorry, the page you requested could not be found.',
    }
    return render(request, 'document_flow/404.html', context, status=404)
