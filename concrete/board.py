import json
import os
import uuid
from datetime import datetime

from project_board_base import ProjectBoardBase

DB_PATH = os.path.join("db", "boards.json")
TEAM_DB = os.path.join("db", "teams.json")
TASKS_DB = os.path.join("db", "tasks.json")


def load_json(path):
    """Load JSON data from file, return empty structure if file doesn't exist."""
    if not os.path.exists(path):
        if "boards" in path:
            return {"boards": []}
        elif "teams" in path:
            return {"teams": []}
        elif "tasks" in path:
            return {"tasks": []}
        else:
            return {}
    
    with open(path, "r") as file:
        return json.load(file)


def save_json(path, data):
    """Save JSON data to file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
        json.dump(data, file, indent=2)


class ProjectBoard(ProjectBoardBase):
    def __init__(self):
        # Ensure db directory and files exist
        os.makedirs("db", exist_ok=True)
        if not os.path.exists(DB_PATH):
            save_json(DB_PATH, {"boards": []})
        if not os.path.exists(TASKS_DB):
            save_json(TASKS_DB, {"tasks": []})

    def create_board(self, request: str) -> str:
        """Create a new board for a team."""
        try:
            data = json.loads(request)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        name = data.get("name", "").strip()
        description = data.get("description", "").strip()
        team_id = data.get("team_id", "").strip()
        creation_time = data.get("creation_time")
        
        # Validation
        if not name:
            raise ValueError("Board name is required")
        if len(name) > 64:
            raise ValueError("Board name must be <= 64 characters")
        if description and len(description) > 128:
            raise ValueError("Description must be <= 128 characters")
        if not team_id:
            raise ValueError("Team ID is required")
        if not creation_time:
            creation_time = datetime.now().isoformat()
        
        # Validate team exists
        teams_data = load_json(TEAM_DB)
        teams = teams_data.get("teams", [])
        if not any(team["id"] == team_id for team in teams):
            raise ValueError("Team ID does not exist")
        
        # Check board name uniqueness within team
        boards_data = load_json(DB_PATH)
        boards = boards_data.get("boards", [])
        
        for board in boards:
            if board["team_id"] == team_id and board["name"] == name:
                raise ValueError("Board name must be unique within the team")
        
        # Create new board
        board_id = str(uuid.uuid4())
        new_board = {
            "id": board_id,
            "name": name,
            "description": description,
            "team_id": team_id,
            "creation_time": creation_time,
            "status": "OPEN",
            "end_time": None
        }
        
        boards.append(new_board)
        boards_data["boards"] = boards
        save_json(DB_PATH, boards_data)
        
        return json.dumps({"id": board_id})

    def close_board(self, request: str) -> str:
        """Close a board if all tasks are complete."""
        try:
            data = json.loads(request)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        board_id = data.get("id")
        if not board_id:
            raise ValueError("Board ID is required")
        
        # Load boards and tasks
        boards_data = load_json(DB_PATH)
        boards = boards_data.get("boards", [])
        tasks_data = load_json(TASKS_DB)
        tasks = tasks_data.get("tasks", [])
        
        board_index = next((i for i, b in enumerate(boards) if b["id"] == board_id), None)
        if board_index is None:
            raise ValueError("Board not found")
        
        if boards[board_index]["status"] == "CLOSED":
            raise ValueError("Board is already closed")
        
        # Check if all tasks are complete
        board_tasks = [t for t in tasks if t["board_id"] == board_id]
        incomplete_tasks = [t for t in board_tasks if t["status"] != "COMPLETE"]
        
        if incomplete_tasks:
            raise ValueError("Cannot close board: not all tasks are complete")
        
        # Close the board
        boards[board_index]["status"] = "CLOSED"
        boards[board_index]["end_time"] = datetime.now().isoformat()
        
        boards_data["boards"] = boards
        save_json(DB_PATH, boards_data)
        
        return json.dumps({"status": "success"})

    def add_task(self, request: str) -> str:
        """Add a task to an open board."""
        try:
            data = json.loads(request)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        user_id = data.get("user_id", "").strip()
        creation_time = data.get("creation_time")
        board_id = data.get("board_id")  # Allow explicit board_id
        
        # Validation
        if not title:
            raise ValueError("Task title is required")
        if len(title) > 64:
            raise ValueError("Task title must be <= 64 characters")
        if description and len(description) > 128:
            raise ValueError("Description must be <= 128 characters")
        if not user_id:
            raise ValueError("User ID is required")
        if not creation_time:
            creation_time = datetime.now().isoformat()
        
        # Load boards and find appropriate board
        boards_data = load_json(DB_PATH)
        boards = boards_data.get("boards", [])
        
        if board_id:
            # Use specific board if provided
            board = next((b for b in boards if b["id"] == board_id), None)
            if not board:
                raise ValueError("Board not found")
            if board["status"] != "OPEN":
                raise ValueError("Can only add tasks to OPEN boards")
        else:
            # Find an open board (for backward compatibility)
            open_boards = [b for b in boards if b["status"] == "OPEN"]
            if not open_boards:
                raise ValueError("No open boards available to add a task")
            board = open_boards[-1]  # Use the latest open board
        
        # Load tasks and check title uniqueness within board
        tasks_data = load_json(TASKS_DB)
        tasks = tasks_data.get("tasks", [])
        
        board_tasks = [t for t in tasks if t["board_id"] == board["id"]]
        if any(task["title"] == title for task in board_tasks):
            raise ValueError("Task title must be unique within the board")
        
        # Create the task
        task_id = str(uuid.uuid4())
        new_task = {
            "id": task_id,
            "title": title,
            "description": description,
            "user_id": user_id,
            "board_id": board["id"],
            "creation_time": creation_time,
            "status": "OPEN"
        }
        
        tasks.append(new_task)
        tasks_data["tasks"] = tasks
        save_json(TASKS_DB, tasks_data)
        
        return json.dumps({"id": task_id})

    def update_task_status(self, request: str):
        """Update the status of a task."""
        try:
            data = json.loads(request)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        task_id = data.get("id")
        status = data.get("status")
        
        if not task_id:
            raise ValueError("Task ID is required")
        if status not in ["OPEN", "IN_PROGRESS", "COMPLETE"]:
            raise ValueError("Status must be one of: OPEN, IN_PROGRESS, COMPLETE")
        
        # Load tasks
        tasks_data = load_json(TASKS_DB)
        tasks = tasks_data.get("tasks", [])
        
        task_index = next((i for i, t in enumerate(tasks) if t["id"] == task_id), None)
        if task_index is None:
            raise ValueError("Task not found")
        
        # Update task status
        tasks[task_index]["status"] = status
        
        tasks_data["tasks"] = tasks
        save_json(TASKS_DB, tasks_data)
        
        return json.dumps({"status": "success"})

    def list_boards(self, request: str) -> str:
        """List all boards for a team."""
        try:
            data = json.loads(request)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        team_id = data.get("id")
        if not team_id:
            raise ValueError("Team ID is required")
        
        # Load boards
        boards_data = load_json(DB_PATH)
        boards = boards_data.get("boards", [])
        
        # Filter boards by team
        team_boards = [b for b in boards if b["team_id"] == team_id]
        
        result = []
        for board in team_boards:
            result.append({
                "id": board["id"],
                "name": board["name"]
            })
        
        return json.dumps(result)

    def export_board(self, request: str) -> str:
        """Export a board to a text file in the out folder."""
        try:
            data = json.loads(request)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        board_id = data.get("id")
        if not board_id:
            raise ValueError("Board ID is required")
        
        # Load board, tasks, and related data
        boards_data = load_json(DB_PATH)
        boards = boards_data.get("boards", [])
        tasks_data = load_json(TASKS_DB)
        tasks = tasks_data.get("tasks", [])
        
        board = next((b for b in boards if b["id"] == board_id), None)
        if not board:
            raise ValueError("Board not found")
        
        # Get board tasks
        board_tasks = [t for t in tasks if t["board_id"] == board_id]
        
        # Create output directory
        os.makedirs("out", exist_ok=True)
        
        # Generate filename
        safe_name = "".join(c for c in board["name"] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"board_{safe_name}_{board_id[:8]}.txt"
        filepath = os.path.join("out", filename)
        
        # Generate export content
        content = []
        content.append("=" * 60)
        content.append(f"BOARD EXPORT: {board['name']}")
        content.append("=" * 60)
        content.append(f"Description: {board.get('description', 'N/A')}")
        content.append(f"Team ID: {board['team_id']}")
        content.append(f"Status: {board['status']}")
        content.append(f"Created: {board['creation_time']}")
        if board.get('end_time'):
            content.append(f"Closed: {board['end_time']}")
        content.append("")
        
        # Task summary
        task_counts = {"OPEN": 0, "IN_PROGRESS": 0, "COMPLETE": 0}
        for task in board_tasks:
            task_counts[task["status"]] += 1
        
        content.append("TASK SUMMARY:")
        content.append("-" * 20)
        content.append(f"Total Tasks: {len(board_tasks)}")
        content.append(f"Open: {task_counts['OPEN']}")
        content.append(f"In Progress: {task_counts['IN_PROGRESS']}")
        content.append(f"Complete: {task_counts['COMPLETE']}")
        content.append("")
        
        # Task details
        if board_tasks:
            content.append("TASK DETAILS:")
            content.append("-" * 30)
            
            for i, task in enumerate(board_tasks, 1):
                content.append(f"{i}. {task['title']} [{task['status']}]")
                content.append(f"   ID: {task['id']}")
                content.append(f"   Description: {task.get('description', 'N/A')}")
                content.append(f"   Assigned to: {task['user_id']}")
                content.append(f"   Created: {task['creation_time']}")
                content.append("")
        else:
            content.append("No tasks found for this board.")
        
        content.append("=" * 60)
        content.append(f"Export generated on: {datetime.now().isoformat()}")
        content.append("=" * 60)
        
        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
        
        return json.dumps({"out_file": filename})