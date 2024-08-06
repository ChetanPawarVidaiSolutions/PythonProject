from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from tasks.views import TaskViewSet
# from projects.views import views
from .views import TaskViewSet, ProjectViewSet, TaskAssignmentViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'task_assignments', TaskAssignmentViewSet, basename='taskassignment')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/<pk>/complete/', TaskViewSet.as_view({'post': 'complete_task'})),
    path('tasks/<pk>/assign/', TaskAssignmentViewSet.as_view({'post': 'assign_task'})),
    path('tasks/<pk>/unassign/', TaskAssignmentViewSet.as_view({'post': 'unassign_task'})),
    path('tasks/<pk>/comments/', CommentViewSet.as_view({'post': 'add_comment'})),
    path('tasks/overdue/', TaskViewSet.as_view({'get': 'get_overdue_tasks'})),
    path('projects/<pk>/progress/', ProjectViewSet.as_view({'post': 'progress'})),
]