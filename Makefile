# Makefile for Team Project Planner
# Industry standard project management commands

.PHONY: help setup install run demo test clean lint format

# Default target
help:
	@echo "Team Project Planner - Available Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup     - Complete project setup (recommended)"
	@echo "  make install   - Install dependencies only"
	@echo ""
	@echo "Running:"
	@echo "  make run       - Start Django development server"
	@echo "  make demo      - Run demo script"
	@echo ""
	@echo "Development:"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Run code linting"
	@echo "  make format    - Format code"
	@echo "  make clean     - Clean temporary files"
	@echo ""
	@echo "Database:"
	@echo "  make migrate   - Run Django migrations"
	@echo "  make reset-db  - Reset database (clear all data)"

# Setup commands
setup:
	@echo "🚀 Running complete project setup..."
	python setup.py

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Running commands
run:
	@echo "🌐 Starting Django development server..."
	python manage.py runserver

demo:
	@echo "🎯 Running demo script..."
	python main.py

# Database commands
migrate:
	@echo "🔧 Running Django migrations..."
	python manage.py migrate

reset-db:
	@echo "🗑️  Resetting database..."
	@if exist db rmdir /s /q db
	@if exist out rmdir /s /q out
	@mkdir db out
	@echo "Database reset complete"

# Development commands
test:
	@echo "🧪 Running tests..."
	@echo "Tests not yet implemented. Add pytest configuration."

lint:
	@echo "🔍 Running code linting..."
	@echo "Linting not configured. Install flake8: pip install flake8"

format:
	@echo "📝 Formatting code..."
	@echo "Formatting not configured. Install black: pip install black"

clean:
	@echo "🧹 Cleaning temporary files..."
	@if exist __pycache__ rmdir /s /q __pycache__
	@if exist "*.pyc" del /q *.pyc
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	@echo "Cleanup complete"
