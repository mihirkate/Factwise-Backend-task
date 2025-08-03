# 🧩 Team Project Planner API

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/django-4.2%2B-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14%2B-red.svg)](https://django-rest-framework.org)

A **file-based API-driven** team project management tool implemented with **abstract base classes** and designed with **industry-standard practices** for modularity, extensibility, and recruiter evaluation.

---

## 📘 Table of Contents

- [📌 Problem Statement](#-problem-statement)
- [🚀 Quick Start](#-quick-start)
- [🏗️ Architecture & Features](#-architecture--features)
- [📁 Project Structure](#-project-structure)
- [📚 Complete API Documentation](#-complete-api-documentation)
- [🧪 Testing Workflow](#-testing-workflow)
- [⚙️ Technical Specifications](#-technical-specifications)

---

## 📌 Problem Statement

Design and implement a **team project planner API** with:

- ✅ **User & Team Management**: CRUD operations with role-based access
- ✅ **Board & Task Management**: Project boards with task lifecycle tracking
- ✅ **File-Based Persistence**: JSON storage (no database required)
- ✅ **RESTful APIs**: Complete HTTP endpoints with proper status codes
- ✅ **Modular Architecture**: Abstract base classes with concrete implementations

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# One-command setup
python setup.py

# Run comprehensive demo
python main.py

# Start API server
python manage.py runserver
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir db out logs

# Start server
python manage.py runserver
```

**🎯 Access Points:**
- **API Base**: `http://localhost:8000/api/`
- **Demo Script**: `python main.py` (creates sample data)
- **Documentation**: This README with copy-paste examples

---

## 🏗️ Architecture & Features

### **🧠 Design Principles**
- ✅ **Abstraction & Modularity**: Clean separation with base classes
- ✅ **Industry Standards**: Professional logging, error handling, validation
- ✅ **File Persistence**: Atomic JSON operations with backup mechanisms
- ✅ **Production Ready**: Configuration management, custom exceptions
- ✅ **Recruiter Friendly**: One-command setup, comprehensive testing

### **🌟 Key Features Implemented**
- ✅ **Modular Architecture**: Base classes → Concrete implementations
- ✅ **CRUD Operations**: Users, Teams, Boards, Tasks with validation
- ✅ **Association Management**: User-team, board-team, task-board relationships
- ✅ **Error Handling**: Custom exception hierarchy with meaningful messages
- ✅ **Export Functionality**: Board export to human-readable text files
- ✅ **Professional Logging**: Configurable levels with file output
- ✅ **Automated Testing**: Demo script with comprehensive workflow

### **⚙️ Assumptions Made**
- 🔹 **Unique Identifiers**: Auto-generated UUIDs for all entities
- 🔹 **File Storage**: JSON-based persistence instead of databases
- 🔹 **Single Access**: Atomic operations for file writing (no concurrent access)
- 🔹 **User Names**: Must be unique across the system
- 🔹 **Team Administration**: Admin users automatically become team members
- 🔹 **Board Lifecycle**: Only boards with all tasks COMPLETE can be closed

---

## 📁 Project Structure

```
factwise-python/
├── config/                 # 🏗️ Configuration Management
│   ├── __init__.py
│   └── settings.py        # Environment-based settings, constants
├── utils/                  # 🔧 Utility Modules  
│   ├── __init__.py
│   ├── exceptions.py      # Custom exception hierarchy
│   ├── file_handler.py    # Atomic file operations with backup
│   ├── logging_config.py  # Professional logging setup
│   └── validators.py      # Comprehensive input validation
├── base/                   # 📐 Abstract Base Classes
│   ├── user_base.py       # User management interface
│   ├── team_base.py       # Team management interface
│   └── board_base.py      # Board management interface
├── concrete/               # 🚀 Production Implementations
│   ├── user.py           # User management with industry standards
│   ├── teams.py          # Team management with validation
│   ├── board.py          # Board & task management
│   ├── views.py          # Django REST API views
│   ├── urls.py           # URL routing configuration
│   └── apps.py           # Django app configuration
├── db/                     # 💾 JSON Data Storage
│   ├── users.json        # User data persistence
│   ├── teams.json        # Team data persistence
│   ├── boards.json       # Board data persistence
│   └── tasks.json        # Task data persistence
├── out/                    # 📄 Generated Exports
│   └── board_*.txt       # Exported board files
├── logs/                   # 📋 Application Logs
├── .venv/                  # 🐍 Virtual Environment
├── factwise/               # ⚙️ Django Project Settings
├── setup.py                # 🚀 Automated Setup Script
├── Makefile               # 🛠️ Project Management Commands
├── main.py                # 🎯 Comprehensive Demo Script
├── manage.py              # 🔧 Django Management
└── requirements.txt       # 📦 Dependencies (Version Pinned)
```

> ⚠️ **Note**: `db/` folder is excluded from version control as per project requirements.

---

## 📚 Complete API Documentation

### **Base URL**: `http://localhost:8000/api`

---

## 👥 User Management APIs

### 1. Create User
- **Method**: `POST` | **Endpoint**: `/api/users/create/`

**Request Body:**
```json
{
  "name": "john_doe",
  "display_name": "John Doe"
}
```

**Success Response (201):**
```json
{
  "id": "ac09bd79-2ef3-4fde-8a63-3b27637c5dd1"
}
```

**PowerShell Example:**
```powershell
$body = @{ name = "john_doe"; display_name = "John Doe" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/users/create/" -Method POST -Body $body -ContentType "application/json"
```

---

### 2. List All Users
- **Method**: `GET` | **Endpoint**: `/api/users/list/`

**Success Response (200):**
```json
[
  {
    "id": "ac09bd79-2ef3-4fde-8a63-3b27637c5dd1",
    "name": "john_doe",
    "display_name": "John Doe",
    "creation_time": "2025-08-04T00:10:15.123456"
  }
]
```

**PowerShell Example:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/users/list/" -Method GET
```

---

### 3. Get User Details
- **Method**: `POST` | **Endpoint**: `/api/users/describe/`

**Request Body:**
```json
{
  "id": "ac09bd79-2ef3-4fde-8a63-3b27637c5dd1"
}
```

---

### 4. Update User
- **Method**: `PUT` | **Endpoint**: `/api/users/update/`

**Request Body:**
```json
{
  "id": "ac09bd79-2ef3-4fde-8a63-3b27637c5dd1",
  "user": {
    "display_name": "John Doe Updated"
  }
}
```

---

### 5. Get User's Teams
- **Method**: `POST` | **Endpoint**: `/api/users/teams/`

**Request Body:**
```json
{
  "id": "ac09bd79-2ef3-4fde-8a63-3b27637c5dd1"
}
```

---

## 🏢 Team Management APIs

### 6. Create Team
- **Method**: `POST` | **Endpoint**: `/api/teams/create/`

**Request Body:**
```json
{
  "name": "dev_team",
  "description": "Development Team",
  "admin": "ac09bd79-2ef3-4fde-8a63-3b27637c5dd1"
}
```

**Success Response (201):**
```json
{
  "id": "dfc6d88c-96e3-4ace-9779-45e4153fe4bc"
}
```

---

### 7. List All Teams
- **Method**: `GET` | **Endpoint**: `/api/teams/list/`

**Success Response (200):**
```json
[
  {
    "id": "dfc6d88c-96e3-4ace-9779-45e4153fe4bc",
    "name": "dev_team",
    "description": "Development Team",
    "admin": "ac09bd79-2ef3-4fde-8a63-3b27637c5dd1",
    "creation_time": "2025-08-04T00:10:17.345678"
  }
]
```

---

### 8. Add Users to Team
- **Method**: `POST` | **Endpoint**: `/api/teams/add_users/`

**Request Body:**
```json
{
  "id": "dfc6d88c-96e3-4ace-9779-45e4153fe4bc",
  "users": [
    "f0cb7919-ba8b-4964-8a6f-72f541b85b65",
    "19c7f65b-e4d0-4b0d-8602-61cfebf343c7"
  ]
}
```

**PowerShell Example:**
```powershell
$teamBody = @{
    id = "dfc6d88c-96e3-4ace-9779-45e4153fe4bc"
    users = @("f0cb7919-ba8b-4964-8a6f-72f541b85b65")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/teams/add_users/" -Method POST -Body $teamBody -ContentType "application/json"
```

---

### 9. List Team Users
- **Method**: `POST` | **Endpoint**: `/api/teams/users/`

**Request Body:**
```json
{
  "id": "dfc6d88c-96e3-4ace-9779-45e4153fe4bc"
}
```

---

## 📋 Board Management APIs

### 10. Create Board
- **Method**: `POST` | **Endpoint**: `/api/boards/create/`

**Request Body:**
```json
{
  "name": "Sprint 1",
  "description": "First development sprint",
  "team_id": "dfc6d88c-96e3-4ace-9779-45e4153fe4bc"
}
```

**Success Response (201):**
```json
{
  "id": "6345d820-cf44-4f6c-b89a-ac983c8bfabb"
}
```

---

### 11. List Team Boards
- **Method**: `POST` | **Endpoint**: `/api/boards/list/`

**Request Body:**
```json
{
  "id": "dfc6d88c-96e3-4ace-9779-45e4153fe4bc"
}
```

---

### 12. Export Board
- **Method**: `POST` | **Endpoint**: `/api/boards/export/`

**Request Body:**
```json
{
  "id": "6345d820-cf44-4f6c-b89a-ac983c8bfabb"
}
```

**Success Response (200):**
```json
{
  "out_file": "out/board_Sprint 1_6345d820.txt"
}
```

---

## ✅ Task Management APIs

### 13. Create Task
- **Method**: `POST` | **Endpoint**: `/api/tasks/create/`

**Request Body:**
```json
{
  "title": "Implement User API",
  "description": "Build REST API endpoints for user management",
  "user_id": "ac09bd79-2ef3-4fde-8a63-3b27637c5dd1",
  "board_id": "6345d820-cf44-4f6c-b89a-ac983c8bfabb"
}
```

**Success Response (201):**
```json
{
  "id": "a05c49cc-5cdc-46ad-97d2-30ce432682ee"
}
```

---

### 14. Update Task Status
- **Method**: `PUT` | **Endpoint**: `/api/tasks/update_status/`

**Request Body:**
```json
{
  "id": "a05c49cc-5cdc-46ad-97d2-30ce432682ee",
  "status": "IN_PROGRESS"
}
```

**Valid Status Values:** `OPEN`, `IN_PROGRESS`, `COMPLETE`

---

## 🧪 Testing Workflow for Recruiters

### **Step 1: Quick Setup & Demo**
```bash
# Automated setup (creates virtual environment, installs dependencies)
python setup.py

# Run comprehensive demo (creates sample data, shows all features)
python main.py

# Start API server
python manage.py runserver
```

### **Step 2: Complete API Testing (Copy & Paste)**

**Create User & Team:**
```powershell
# Create user
$user = @{ name = "alice_dev"; display_name = "Alice Developer" } | ConvertTo-Json
$userResult = Invoke-RestMethod -Uri "http://localhost:8000/api/users/create/" -Method POST -Body $user -ContentType "application/json"
Write-Host "User ID: $($userResult.id)"

# Create team
$team = @{ name = "api_test_team"; description = "API Testing Team"; admin = $userResult.id } | ConvertTo-Json
$teamResult = Invoke-RestMethod -Uri "http://localhost:8000/api/teams/create/" -Method POST -Body $team -ContentType "application/json"
Write-Host "Team ID: $($teamResult.id)"
```

**Create Board & Task:**
```powershell
# Create board
$board = @{ name = "API_Test_Board"; description = "Testing Board"; team_id = $teamResult.id } | ConvertTo-Json
$boardResult = Invoke-RestMethod -Uri "http://localhost:8000/api/boards/create/" -Method POST -Body $board -ContentType "application/json"
Write-Host "Board ID: $($boardResult.id)"

# Create task
$task = @{ title = "API_Task"; description = "Test task"; user_id = $userResult.id; board_id = $boardResult.id } | ConvertTo-Json
$taskResult = Invoke-RestMethod -Uri "http://localhost:8000/api/tasks/create/" -Method POST -Body $task -ContentType "application/json"
Write-Host "Task ID: $($taskResult.id)"

# Update task status
$status = @{ id = $taskResult.id; status = "COMPLETE" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/tasks/update_status/" -Method PUT -Body $status -ContentType "application/json"
Write-Host "Task marked as COMPLETE"
```

**List & Export:**
```powershell
# List all users
Write-Host "=== USERS ==="
Invoke-RestMethod -Uri "http://localhost:8000/api/users/list/" -Method GET

# List all teams
Write-Host "=== TEAMS ==="
Invoke-RestMethod -Uri "http://localhost:8000/api/teams/list/" -Method GET

# Export board
$export = @{ id = $boardResult.id } | ConvertTo-Json
$exportResult = Invoke-RestMethod -Uri "http://localhost:8000/api/boards/export/" -Method POST -Body $export -ContentType "application/json"
Write-Host "Board exported to: $($exportResult.out_file)"
```

### **Step 3: Verify Generated Files**
```bash
# Check database files
ls db/  # Should show: users.json, teams.json, boards.json, tasks.json

# Check exported files
ls out/  # Should show: board_*.txt files

# Check logs
ls logs/  # Should show application logs
```

---

## ⚙️ Technical Specifications

### **🔧 Tech Stack**
- **Language**: Python 3.8+
- **Framework**: Django 4.2+ with Django REST Framework 3.14+
- **Storage**: Local JSON files (atomic operations)
- **Architecture**: Abstract base classes with concrete implementations
- **Testing**: PowerShell scripts, cURL, Postman compatible

### **📋 Business Rules & Constraints**

**Users:**
- User names must be unique and ≤ 64 characters
- Display names ≤ 64 characters (128 for updates)
- User names cannot be changed after creation

**Teams:**
- Team names must be unique and ≤ 64 characters
- Descriptions ≤ 128 characters
- Maximum 50 users per team
- Admin users are automatically team members

**Boards:**
- Board names must be unique within a team and ≤ 64 characters
- Descriptions ≤ 128 characters
- Boards can be OPEN or CLOSED
- Only boards with all tasks COMPLETE can be closed

**Tasks:**
- Task titles must be unique within a board and ≤ 64 characters
- Descriptions ≤ 128 characters
- Tasks can only be added to OPEN boards
- Task statuses: OPEN, IN_PROGRESS, COMPLETE

### **⚠️ Error Responses**

**400 Bad Request:**
```json
{ "error": "Validation failed: User name must be unique" }
```

**404 Not Found:**
```json
{ "error": "User not found" }
```

**500 Internal Server Error:**
```json
{ "error": "Internal server error" }
```

---

## 🎯 Key Highlights for Recruiters

### **✅ Senior-Level Skills Demonstrated:**
- **Clean Architecture**: Abstract base classes → Concrete implementations
- **Industry Standards**: Professional logging, error handling, validation
- **Production Ready**: Configuration management, custom exceptions
- **Documentation**: Comprehensive API docs with copy-paste examples
- **Testing**: Automated setup, demo script, comprehensive workflow

### **✅ Python/Django Excellence:**
- Django REST Framework best practices
- Proper URL routing and view structure
- Custom validation and exception handling
- Professional project structure
- Version-pinned dependencies

### **✅ Evaluation Benefits:**
- **5-minute setup**: One command (`python setup.py`)
- **Immediate demo**: `python main.py` shows all features
- **Copy-paste testing**: PowerShell scripts ready to use
- **File verification**: Generated exports and database files
- **Professional code**: Industry-standard architecture patterns

---

**🚀 Ready for immediate evaluation with professional-grade code quality!**
