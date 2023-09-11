from django.contrib.auth.views import LoginView
from django.urls import path, re_path

from document_flow.views import CustomLogoutView, index

from . import views

app_name = 'document_flow'

urlpatterns = [
    path('', index, name='index'),
    path('create_user/', views.create_user, name='create_user'),
    path('user/<int:id>/', views.user_detail, name='user_detail'),
    path('user_list/', views.user_list, name='user_list'),
    path('update_user/<int:id>/', views.update_user, name='update_user'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    re_path(r'^get_documents/?$', views.get_documents, name='get_documents'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/detail/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/delete/<int:pk>/', views.delete_project, name='delete_project'),
    path('documents/', views.get_documents, name='get_documents'),
    path('documents/create/', views.create_document, name='create_document'),
    path('documents/update/<int:pk>/', views.update_document, name='update_document'),
    path('documents/delete/<int:pk>/', views.delete_document, name='delete_document'),
]
