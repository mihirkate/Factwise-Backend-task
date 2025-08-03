import json
import os
import uuid
from datetime import datetime

from base.team_base import TeamBase

DB_PATH = os.path.join("db", "teams.json")
USERS_DB_PATH = os.path.join("db", "users.json")


def load_json(path):
    """Load JSON data from file, return empty structure if file doesn't exist."""
    if not os.path.exists(path):
        return {"teams": []} if "teams" in path else {"users": []}
    
    with open(path, "r") as file:
        return json.load(file)


def save_json(path, data):
    """Save JSON data to file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
        json.dump(data, file, indent=2)


class Teams(TeamBase):
    def __init__(self):
        # Ensure db directory and files exist
        os.makedirs("db", exist_ok=True)
        if not os.path.exists(DB_PATH):
            save_json(DB_PATH, {"teams": []})

    def create_team(self, request: str) -> str:
        """Create a new team with unique name."""
        try:
            data = json.loads(request)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        name = data.get("name", "").strip()
        description = data.get("description", "").strip()
        admin = data.get("admin", "").strip()
        
        # Validation
        if not name:
            raise ValueError("Team name is required")
        if len(name) > 64:
            raise ValueError("Team name must be <= 64 characters")
        if len(description) > 128:
            raise ValueError("Description must be <= 128 characters")
        if not admin:
            raise ValueError("Admin user ID is required")
        
        # Validate admin user exists
        users_data = load_json(USERS_DB_PATH)
        users = users_data.get("users", [])
        if not any(user["id"] == admin for user in users):
            raise ValueError("Admin user does not exist")
        
        # Load existing teams and check uniqueness
        db_data = load_json(DB_PATH)
        teams = db_data.get("teams", [])
        
        if any(team["name"] == name for team in teams):
            raise ValueError("Team name must be unique")
        
        # Create new team
        team_id = str(uuid.uuid4())
        new_team = {
            "id": team_id,
            "name": name,
            "description": description,
            "admin": admin,
            "members": [admin],  # Admin is automatically a member
            "creation_time": datetime.now().isoformat()
        }
        
        teams.append(new_team)
        db_data["teams"] = teams
        save_json(DB_PATH, db_data)
        
        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        """List all teams."""
        db_data = load_json(DB_PATH)
        teams = db_data.get("teams", [])
        
        result = []
        for team in teams:
            result.append({
                "name": team["name"],
                "description": team["description"],
                "creation_time": team["creation_time"],
                "admin": team["admin"]
            })
        
        return json.dumps(result)

    def describe_team(self, request: str) -> str:
        """Get details of a specific team."""
        try:
            data = json.loads(request)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        team_id = data.get("id")
        if not team_id:
            raise ValueError("Team ID is required")
        
        db_data = load_json(DB_PATH)
        teams = db_data.get("teams", [])
        
        team = next((t for t in teams if t["id"] == team_id), None)
        if not team:
            raise ValueError("Team not found")
        
        return json.dumps({
            "name": team["name"],
            "description": team["description"],
            "creation_time": team["creation_time"],
            "admin": team["admin"]
        })

    def update_team(self, request: str) -> str:
        """Update team details with unique name constraint."""
        try:
            data = json.loads(request)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        team_id = data.get("id")
        team_data = data.get("team", {})
        
        if not team_id:
            raise ValueError("Team ID is required")
        
        name = team_data.get("name", "").strip()
        description = team_data.get("description", "").strip()
        admin = team_data.get("admin", "").strip()
        
        # Validation
        if name and len(name) > 64:
            raise ValueError("Team name must be <= 64 characters")
        if description and len(description) > 128:
            raise ValueError("Description must be <= 128 characters")
        
        db_data = load_json(DB_PATH)
        teams = db_data.get("teams", [])
        
        team_index = next((i for i, t in enumerate(teams) if t["id"] == team_id), None)
        if team_index is None:
            raise ValueError("Team not found")
        
        # Check name uniqueness (excluding current team)
        if name and any(t["name"] == name and t["id"] != team_id for t in teams):
            raise ValueError("Team name must be unique")
        
        # Validate admin user exists if provided
        if admin:
            users_data = load_json(USERS_DB_PATH)
            users = users_data.get("users", [])
            if not any(user["id"] == admin for user in users):
                raise ValueError("Admin user does not exist")
            
            # Ensure admin is in members list
            if admin not in teams[team_index]["members"]:
                teams[team_index]["members"].append(admin)
        
        # Update team
        if name:
            teams[team_index]["name"] = name
        if description:
            teams[team_index]["description"] = description
        if admin:
            teams[team_index]["admin"] = admin
        
        db_data["teams"] = teams
        save_json(DB_PATH, db_data)
        
        return json.dumps({"status": "success"})

    def add_users_to_team(self, request: str):
        """Add users to a team with max 50 users constraint."""
        try:
            data = json.loads(request)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        team_id = data.get("id")
        user_ids = data.get("users", [])
        
        if not team_id:
            raise ValueError("Team ID is required")
        if not isinstance(user_ids, list):
            raise ValueError("Users must be a list")
        
        # Validate users exist
        users_data = load_json(USERS_DB_PATH)
        existing_users = {user["id"] for user in users_data.get("users", [])}
        
        for user_id in user_ids:
            if user_id not in existing_users:
                raise ValueError(f"User {user_id} does not exist")
        
        db_data = load_json(DB_PATH)
        teams = db_data.get("teams", [])
        
        team_index = next((i for i, t in enumerate(teams) if t["id"] == team_id), None)
        if team_index is None:
            raise ValueError("Team not found")
        
        current_members = set(teams[team_index].get("members", []))
        new_members = current_members.union(set(user_ids))
        
        # Check 50 user limit
        if len(new_members) > 50:
            raise ValueError("Cannot add users: team would exceed 50 member limit")
        
        teams[team_index]["members"] = list(new_members)
        db_data["teams"] = teams
        save_json(DB_PATH, db_data)
        
        return json.dumps({"status": "success"})

    def remove_users_from_team(self, request: str):
        """Remove users from a team."""
        try:
            data = json.loads(request)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        team_id = data.get("id")
        user_ids = data.get("users", [])
        
        if not team_id:
            raise ValueError("Team ID is required")
        if not isinstance(user_ids, list):
            raise ValueError("Users must be a list")
        
        db_data = load_json(DB_PATH)
        teams = db_data.get("teams", [])
        
        team_index = next((i for i, t in enumerate(teams) if t["id"] == team_id), None)
        if team_index is None:
            raise ValueError("Team not found")
        
        current_members = set(teams[team_index].get("members", []))
        admin_id = teams[team_index]["admin"]
        
        # Don't allow removing the admin
        if admin_id in user_ids:
            raise ValueError("Cannot remove team admin from team")
        
        new_members = current_members - set(user_ids)
        teams[team_index]["members"] = list(new_members)
        
        db_data["teams"] = teams
        save_json(DB_PATH, db_data)
        
        return json.dumps({"status": "success"})

    def list_team_users(self, request: str):
        """List all users in a team."""
        try:
            data = json.loads(request)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        
        team_id = data.get("id")
        if not team_id:
            raise ValueError("Team ID is required")
        
        db_data = load_json(DB_PATH)
        teams = db_data.get("teams", [])
        
        team = next((t for t in teams if t["id"] == team_id), None)
        if not team:
            raise ValueError("Team not found")
        
        # Get user details
        users_data = load_json(USERS_DB_PATH)
        users = {user["id"]: user for user in users_data.get("users", [])}
        
        result = []
        for user_id in team.get("members", []):
            if user_id in users:
                user = users[user_id]
                result.append({
                    "id": user["id"],
                    "name": user["name"],
                    "display_name": user["display_name"]
                })
        
        return json.dumps(result)