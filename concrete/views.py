import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View

from .user import User
from .teams import Teams
from .board import ProjectBoard


class BaseAPIView(View):
    """Base view for all API endpoints with common error handling."""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Internal server error"}, status=500)


# User Management Views
class UserCreateView(BaseAPIView):
    def post(self, request):
        user_manager = User()
        result = user_manager.create_user(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result), status=201)


class UserListView(BaseAPIView):
    def get(self, request):
        user_manager = User()
        result = user_manager.list_users()
        return JsonResponse(json.loads(result), safe=False)


class UserDetailView(BaseAPIView):
    def post(self, request):
        user_manager = User()
        result = user_manager.describe_user(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result))


class UserUpdateView(BaseAPIView):
    def put(self, request):
        user_manager = User()
        result = user_manager.update_user(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result))


class UserTeamsView(BaseAPIView):
    def post(self, request):
        user_manager = User()
        result = user_manager.get_user_teams(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result), safe=False)


# Team Management Views
class TeamCreateView(BaseAPIView):
    def post(self, request):
        team_manager = Teams()
        result = team_manager.create_team(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result), status=201)


class TeamListView(BaseAPIView):
    def get(self, request):
        team_manager = Teams()
        result = team_manager.list_teams()
        return JsonResponse(json.loads(result), safe=False)


class TeamDetailView(BaseAPIView):
    def post(self, request):
        team_manager = Teams()
        result = team_manager.describe_team(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result))


class TeamUpdateView(BaseAPIView):
    def put(self, request):
        team_manager = Teams()
        result = team_manager.update_team(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result))


class TeamAddUsersView(BaseAPIView):
    def post(self, request):
        team_manager = Teams()
        result = team_manager.add_users_to_team(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result))


class TeamRemoveUsersView(BaseAPIView):
    def post(self, request):
        team_manager = Teams()
        result = team_manager.remove_users_from_team(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result))


class TeamUsersView(BaseAPIView):
    def post(self, request):
        team_manager = Teams()
        result = team_manager.list_team_users(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result), safe=False)


# Board Management Views
class BoardCreateView(BaseAPIView):
    def post(self, request):
        board_manager = ProjectBoard()
        result = board_manager.create_board(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result), status=201)


class BoardCloseView(BaseAPIView):
    def post(self, request):
        board_manager = ProjectBoard()
        result = board_manager.close_board(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result))


class TaskCreateView(BaseAPIView):
    def post(self, request):
        board_manager = ProjectBoard()
        result = board_manager.add_task(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result), status=201)


class TaskUpdateView(BaseAPIView):
    def put(self, request):
        board_manager = ProjectBoard()
        result = board_manager.update_task_status(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result))


class BoardListView(BaseAPIView):
    def post(self, request):
        board_manager = ProjectBoard()
        result = board_manager.list_boards(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result), safe=False)


class BoardExportView(BaseAPIView):
    def post(self, request):
        board_manager = ProjectBoard()
        result = board_manager.export_board(request.body.decode('utf-8'))
        return JsonResponse(json.loads(result))