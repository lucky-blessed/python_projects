#!/usr/bin/env python3
"""
Task Tracker CLI
A simple command line application to manage tasks.
"""

import sys

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