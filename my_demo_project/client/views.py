from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer
from django.contrib.auth.models import User

# List and Create Clients
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Retrieve, Update, and Delete Client
class ClientRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

# Create a new project for a client and assign users
class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        client = Client.objects.get(pk=self.kwargs['client_id'])
        serializer.save(client=client, created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        project_data = request.data
        project = Project.objects.create(
            project_name=project_data['project_name'],
            client_id=kwargs['client_id'],
            created_by=request.user
        )
        users = User.objects.filter(id__in=[user['id'] for user in project_data['users']])
        project.users.set(users)
        return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)

# List all projects assigned to the logged-in user
class UserAssignedProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.assigned_projects.all()
