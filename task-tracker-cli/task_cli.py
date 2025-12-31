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
    print(f"Command recieved: {command}")



if __name__ == "__main__":
    main()