#!/usr/bin/env python3
"""
Task Tracker CLI
A simple command line application to manage tasks.
"""

import sys
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    """
    To load tasks from JSON file.
    Create an empty one if the file does not exist.
    Returns a list of tasks.
    """

    # Checks if the tasks file exists
    if not os.path.exists(TASKS_FILE):
        # If it does not exit, create it with an empty list
        with open(TASKS_FILE, "w") as file:
            json.dump([], file)
        return []
    
    # If file exists, try to read it
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Handles corrupted JSON file
        print("Error: tasks.json is corrupted.")
        return []
    
def save_tasks(tasks):
    """
    Saves the list of tasks to the JSON file.
    """

    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)


def generate_task_id(tasks):
    """
    Generates a unique task ID.
    Use the highest existing ID + 1.
    """

    if not tasks:
        return 1
    
    # Get the highest ID currently in the list
    max_id = max(task["id"] for task in tasks)
    return max_id + 1


def add_task(description):
    """
    Adds a new task with a unique ID and timestamps:
    """

    tasks = load_tasks()

    task_id = generate_task_id(tasks)
    time_now = datetime.now().isoformat()

    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": time_now,
        "updatedAt": time_now
    }

    tasks.append(new_task)
    save_tasks(tasks)

    print(f"Task added successfully (ID: {task_id})")


def list_tasks(status=None):
    """
    List tasks.
    If status is provided, filter tasks by that status.
    """
    tasks = load_tasks()

    # If there are no tasks at all
    if not tasks:
        print("No tasks found.")
        return
    
    # Filter tasks if a status is specified
    if status:
        tasks = [task for task in tasks if task["status"] == status]

        if not tasks:
            print(f"No tasks with status '{status}'.")
            return
    
    # Display tasks
    for task in tasks:
        created_date = task["createdAt"].split("T")[0]
        print(
            f"[{task['id']}] "
            f"{task['description']} | "
            f"{task['status']} | "
            f"{created_date}"
        )
        

def main():
    """
    Entry point of the Task Tracker CLI.
    Reads command line arguments and routes commands.
    """


    # sys.argv contains all command line arguments 
    # Example: ['task_cli.py', 'add', 'Buy groceries']
    args = sys.argv

    # If no command is provided
    if len(args) < 2:
        print("Error: No command provided.")
        print("Usage: python task-cli.py <command> [arguments]")
        return
    
    command = args[1]

    if command == "add":
        if len(args) < 3:
            print("Error: Task description required")
            return
        
        description = args[2]
        add_task(description)
    else:
        print("Error: Unknown command")


if __name__ == "__main__":
    main()