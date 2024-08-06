from django.shortcuts import render
from rest_framework.response import Response
import logging

# Create your views here.
# tasks/views.py
from django.shortcuts import render
from rest_framework import viewsets
from .models import Task, Project, TaskAssignment, Comment
from .serializers import TaskSerializer, ProjectSerializer, TaskAssignmentSerializer, CommentSerializer

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_overdue_tasks(self, request):
        tasks = Task.objects.filter(due_date__lt=datetime.date.today())
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def complete_task(self, request, pk):
        task = self.get_object()
        if task.status == 'In Progress':
            task.status = 'Completed'
            task.save()
            return Response({'message': 'Task completed successfully'})
        return Response({'error': 'Task is not in progress'}, status=400)
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def calculate_progress(self, request, pk):
        project = self.get_object()
        completed_tasks = project.tasks.filter(status='Completed')
        total_tasks = project.tasks.count()
        progress = (completed_tasks.count() / total_tasks) * 100
        return Response({'progress': progress})
    
    def handle_exception(self, exc):
        logger.error(f"Error in ProjectViewSet: {str(exc)}")
        return Response({"error": str(exc)}, status=500)

class TaskAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAssignment.objects.all()
    serializer_class = TaskAssignmentSerializer
    
    def assign_task(self, request, pk):
        task = Task.objects.get(pk=pk)
        user = User.objects.get(pk=request.data['user_id'])
        TaskAssignment.objects.create(task=task, user=user)
        return Response({'message': 'Task assigned successfully'})

    def unassign_task(self, request, pk):
        task = Task.objects.get(pk=pk)
        user = User.objects.get(pk=request.data['user_id'])
        TaskAssignment.objects.filter(task=task, user=user).delete()
        return Response({'message': 'Task unassigned successfully'})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def add_comment(self, request, pk):
        task = Task.objects.get(pk=pk)
        user = User.objects.get(pk=request.data['user_id'])
        comment = Comment.objects.create(task=task, user=user, text=request.data['text'])
        return Response({'message': 'Comment added successfully'})
