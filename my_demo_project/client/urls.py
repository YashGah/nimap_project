from django.urls import path
from .views import ClientListCreateView, ClientRetrieveUpdateDeleteView, ProjectCreateView, UserAssignedProjectsView

urlpatterns = [
    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDeleteView.as_view(), name='client-detail'),
    path('clients/<int:client_id>/projects/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/', UserAssignedProjectsView.as_view(), name='user-assigned-projects'),
]
