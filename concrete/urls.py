from django.urls import path
from . import views

urlpatterns = [
    # User Management URLs
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/list/', views.UserListView.as_view(), name='user-list'),
    path('users/describe/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('users/teams/', views.UserTeamsView.as_view(), name='user-teams'),
    
    # Team Management URLs
    path('teams/create/', views.TeamCreateView.as_view(), name='team-create'),
    path('teams/list/', views.TeamListView.as_view(), name='team-list'),
    path('teams/describe/', views.TeamDetailView.as_view(), name='team-detail'),
    path('teams/update/', views.TeamUpdateView.as_view(), name='team-update'),
    path('teams/add_users/', views.TeamAddUsersView.as_view(), name='team-add-users'),
    path('teams/remove_users/', views.TeamRemoveUsersView.as_view(), name='team-remove-users'),
    path('teams/users/', views.TeamUsersView.as_view(), name='team-users'),
    
    # Board Management URLs
    path('boards/create/', views.BoardCreateView.as_view(), name='board-create'),
    path('boards/close/', views.BoardCloseView.as_view(), name='board-close'),
    path('boards/list/', views.BoardListView.as_view(), name='board-list'),
    path('boards/export/', views.BoardExportView.as_view(), name='board-export'),
    
    # Task Management URLs
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/update_status/', views.TaskUpdateView.as_view(), name='task-update'),
]