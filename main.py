#!/usr/bin/env python3
"""
Main demo script for Team Project Planner.

This script demonstrates the comprehensive functionality of the Team Project Planner
with industry-standard logging and error handling. It showcases user management,
team management, and board/task management capabilities.

Usage:
    python main.py

The script will:
1. Initialize logging and configuration
2. Create sample users with proper validation
3. Demonstrate team management features
4. Show board and task lifecycle management
5. Generate exported board files
6. Provide comprehensive output and error handling
"""

import json
import os
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import project modules
from config.settings import get_config
from utils.logging_config import setup_logging, get_logger
from utils.exceptions import TeamPlannerException
from concrete.user import User
from concrete.teams import Teams
from concrete.board import ProjectBoard

# Initialize configuration and logging
config = get_config('development')
setup_logging(config.LOG_LEVEL, 'logs/demo.log')
logger = get_logger(__name__)

class DemoRunner:
    """
    Comprehensive demo runner for Team Project Planner.
    
    Demonstrates all major functionality with proper error handling
    and comprehensive logging.
    """
    
    def __init__(self):
        """Initialize demo runner with managers."""
        self.user_manager = User()
        self.team_manager = Teams()
        self.board_manager = ProjectBoard()
        logger.info("Demo runner initialized")
    
    def cleanup_previous_data(self):
        """Clean up any previous demo data."""
        logger.info("Cleaning up previous demo data")
        
        db_files = [
            config.USERS_DB_PATH,
            config.TEAMS_DB_PATH, 
            config.BOARDS_DB_PATH,
            config.TASKS_DB_PATH
        ]
        
        for file_path in db_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    logger.debug(f"Removed existing file: {file_path}")
                except Exception as e:
                    logger.warning(f"Could not remove {file_path}: {e}")
    
    def demo_user_management(self):
        """Demonstrate comprehensive user management functionality."""
        logger.info("=== STARTING USER MANAGEMENT DEMO ===")
        print("\n=== USER MANAGEMENT DEMO ===")
        
        # Sample user data with various scenarios
        users_data = [
            {"name": "john_doe", "display_name": "John Doe"},
            {"name": "jane_smith", "display_name": "Jane Smith"},
            {"name": "bob_wilson", "display_name": "Bob Wilson"},
            {"name": "alice_johnson", "display_name": "Alice Johnson"}
        ]
        
        user_ids = []
        
        print("Creating users...")
        for user_data in users_data:
            try:
                result = self.user_manager.create_user(json.dumps(user_data))
                user_id = json.loads(result)["id"]
                user_ids.append(user_id)
                print(f"✅ Created user: {user_data['name']} (ID: {user_id[:8]}...)")
                logger.info(f"User created: {user_data['name']} with ID: {user_id}")
                
            except TeamPlannerException as e:
                print(f"❌ Error creating user {user_data['name']}: {e}")
                logger.error(f"Failed to create user {user_data['name']}: {e}")
        
        # Demonstrate user listing
        print(f"\nListing all {len(user_ids)} users:")
        try:
            users_list = json.loads(self.user_manager.list_users())
            for user in users_list:
                print(f"  • {user['name']} ({user['display_name']})")
                
        except TeamPlannerException as e:
            print(f"❌ Error listing users: {e}")
            logger.error(f"Failed to list users: {e}")
        
        # Demonstrate user update
        if user_ids:
            print(f"\nUpdating display name for user {user_ids[0][:8]}...")
            update_data = {
                "id": user_ids[0],
                "user": {"display_name": "John Doe (Updated)"}
            }
            try:
                self.user_manager.update_user(json.dumps(update_data))
                print("✅ User updated successfully")
                logger.info(f"User updated: {user_ids[0]}")
                
            except TeamPlannerException as e:
                print(f"❌ Error updating user: {e}")
                logger.error(f"Failed to update user: {e}")
        
        logger.info(f"User management demo completed. Created {len(user_ids)} users")
        return user_ids
    
    def demo_team_management(self, user_ids):
        """Demonstrate comprehensive team management functionality."""
        logger.info("=== STARTING TEAM MANAGEMENT DEMO ===")
        print("\n=== TEAM MANAGEMENT DEMO ===")
        
        if not user_ids:
            print("❌ No users available for team demo")
            logger.warning("No users available for team demo")
            return []
        
        # Sample team data
        teams_data = [
            {
                "name": "dev_team", 
                "description": "Development Team", 
                "admin": user_ids[0]
            },
            {
                "name": "qa_team", 
                "description": "Quality Assurance Team", 
                "admin": user_ids[1] if len(user_ids) > 1 else user_ids[0]
            }
        ]
        
        team_ids = []
        
        print("Creating teams...")
        for team_data in teams_data:
            try:
                result = self.team_manager.create_team(json.dumps(team_data))
                team_id = json.loads(result)["id"]
                team_ids.append(team_id)
                print(f"✅ Created team: {team_data['name']} (ID: {team_id[:8]}...)")
                logger.info(f"Team created: {team_data['name']} with ID: {team_id}")
                
            except TeamPlannerException as e:
                print(f"❌ Error creating team {team_data['name']}: {e}")
                logger.error(f"Failed to create team {team_data['name']}: {e}")
        
        # Demonstrate adding users to teams
        if team_ids and len(user_ids) > 1:
            print(f"\nAdding users to team {team_ids[0][:8]}...")
            add_users_data = {
                "id": team_ids[0],
                "users": user_ids[1:3]  # Add 2 additional users
            }
            try:
                self.team_manager.add_users_to_team(json.dumps(add_users_data))
                print("✅ Users added to team successfully")
                logger.info(f"Added users to team: {team_ids[0]}")
                
            except TeamPlannerException as e:
                print(f"❌ Error adding users to team: {e}")
                logger.error(f"Failed to add users to team: {e}")
        
        # Demonstrate team user listing
        if team_ids:
            print(f"\nListing users in team {team_ids[0][:8]}...")
            list_users_data = {"id": team_ids[0]}
            try:
                team_users = json.loads(self.team_manager.list_team_users(json.dumps(list_users_data)))
                for user in team_users:
                    print(f"  • {user['name']} ({user['display_name']})")
                    
            except TeamPlannerException as e:
                print(f"❌ Error listing team users: {e}")
                logger.error(f"Failed to list team users: {e}")
        
        logger.info(f"Team management demo completed. Created {len(team_ids)} teams")
        return team_ids
    
    def demo_board_management(self, team_ids, user_ids):
        """Demonstrate comprehensive board and task management functionality."""
        logger.info("=== STARTING BOARD & TASK MANAGEMENT DEMO ===")
        print("\n=== BOARD & TASK MANAGEMENT DEMO ===")
        
        if not team_ids or not user_ids:
            print("❌ No teams or users available for board demo")
            logger.warning("No teams or users available for board demo")
            return
        
        # Sample board data
        boards_data = [
            {
                "name": "Sprint_1",
                "description": "First development sprint with user stories",
                "team_id": team_ids[0]
            },
            {
                "name": "Testing_Board",
                "description": "QA testing and bug tracking board",
                "team_id": team_ids[0]
            }
        ]
        
        board_ids = []
        
        print("Creating boards...")
        for board_data in boards_data:
            try:
                result = self.board_manager.create_board(json.dumps(board_data))
                board_id = json.loads(result)["id"]
                board_ids.append(board_id)
                print(f"✅ Created board: {board_data['name']} (ID: {board_id[:8]}...)")
                logger.info(f"Board created: {board_data['name']} with ID: {board_id}")
                
            except TeamPlannerException as e:
                print(f"❌ Error creating board {board_data['name']}: {e}")
                logger.error(f"Failed to create board {board_data['name']}: {e}")
        
        # Demonstrate task creation
        if board_ids:
            print(f"\nAdding tasks to board {board_ids[0][:8]}...")
            tasks_data = [
                {
                    "title": "Implement_User_API",
                    "description": "Build REST API endpoints for user management",
                    "user_id": user_ids[0],
                    "board_id": board_ids[0]
                },
                {
                    "title": "Write_Unit_Tests",
                    "description": "Create comprehensive unit tests for API",
                    "user_id": user_ids[1] if len(user_ids) > 1 else user_ids[0],
                    "board_id": board_ids[0]
                },
                {
                    "title": "API_Documentation", 
                    "description": "Write comprehensive API documentation",
                    "user_id": user_ids[2] if len(user_ids) > 2 else user_ids[0],
                    "board_id": board_ids[0]
                },
                {
                    "title": "Performance_Testing",
                    "description": "Conduct performance and load testing",
                    "user_id": user_ids[3] if len(user_ids) > 3 else user_ids[0],
                    "board_id": board_ids[0]
                }
            ]
            
            task_ids = []
            for task_data in tasks_data:
                try:
                    result = self.board_manager.add_task(json.dumps(task_data))
                    task_id = json.loads(result)["id"]
                    task_ids.append(task_id)
                    print(f"✅ Created task: {task_data['title']} (ID: {task_id[:8]}...)")
                    logger.info(f"Task created: {task_data['title']} with ID: {task_id}")
                    
                except TeamPlannerException as e:
                    print(f"❌ Error creating task {task_data['title']}: {e}")
                    logger.error(f"Failed to create task {task_data['title']}: {e}")
            
            # Demonstrate task status updates
            if task_ids:
                print("\nUpdating task statuses...")
                status_updates = [
                    {"id": task_ids[0], "status": "COMPLETE"},
                    {"id": task_ids[1], "status": "COMPLETE"} if len(task_ids) > 1 else None,
                    {"id": task_ids[2], "status": "IN_PROGRESS"} if len(task_ids) > 2 else None,
                    {"id": task_ids[3], "status": "OPEN"} if len(task_ids) > 3 else None
                ]
                
                for update in status_updates:
                    if update:
                        try:
                            self.board_manager.update_task_status(json.dumps(update))
                            print(f"✅ Updated task {update['id'][:8]}... to {update['status']}")
                            logger.info(f"Task status updated: {update['id']} to {update['status']}")
                            
                        except TeamPlannerException as e:
                            print(f"❌ Error updating task status: {e}")
                            logger.error(f"Failed to update task status: {e}")
        
        # Demonstrate board export
        if board_ids:
            print(f"\nExporting board {board_ids[0][:8]}...")
            export_data = {"id": board_ids[0]}
            try:
                result = self.board_manager.export_board(json.dumps(export_data))
                filename = json.loads(result)["out_file"]
                print(f"✅ Board exported to: out/{filename}")
                logger.info(f"Board exported: {filename}")
                
            except TeamPlannerException as e:
                print(f"❌ Error exporting board: {e}")
                logger.error(f"Failed to export board: {e}")
        
        logger.info("Board and task management demo completed")
    
    def run_complete_demo(self):
        """Run the complete demonstration workflow."""
        logger.info("Starting complete Team Project Planner demonstration")
        print("🚀 Team Project Planner - Comprehensive Demo")
        print("=" * 60)
        
        try:
            # Optional: Clean up previous data for fresh demo
            # self.cleanup_previous_data()
            
            # Run demo sections
            user_ids = self.demo_user_management()
            team_ids = self.demo_team_management(user_ids)
            self.demo_board_management(team_ids, user_ids)
            
            # Summary
            print("\n" + "=" * 60)
            print("🎉 DEMO COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"✅ Created {len(user_ids)} users")
            print(f"✅ Created {len(team_ids)} teams")
            print("✅ Created boards and tasks")
            print("✅ Demonstrated status updates")
            print("✅ Generated board export")
            print("\n📁 Generated Files:")
            print("   • db/ - All data files (users, teams, boards, tasks)")
            print("   • out/ - Exported board files")
            print("   • logs/ - Application and demo logs")
            print("\n🌐 Next Steps:")
            print("   • Run 'python manage.py runserver' to start API server")
            print("   • Visit http://localhost:8000/api/ for REST endpoints")
            print("   • Check README.md for complete API documentation")
            
            logger.info("Complete demonstration finished successfully")
            
        except Exception as e:
            print(f"\n❌ Demo failed with error: {e}")
            logger.error(f"Demo failed: {e}", exc_info=True)
            raise

def main():
    """Main entry point for the demo script."""
    try:
        demo_runner = DemoRunner()
        demo_runner.run_complete_demo()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        logger.info("Demo interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        logger.critical(f"Fatal error in demo: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()