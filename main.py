import json
import os
import sys
from datetime import datetime

def load_tasks():
    file_name = 'task.json'
    
    # 1. If file doesn't exist, return empty list
    if not os.path.exists(file_name):
        return []
    
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            return data
    except (json.JSONDecodeError, ValueError):
        return []

def save_tasks(tasks):
    file_name='task.json'
    
    try:
        with open(file_name, 'w') as file:
            json.dump(tasks, file, indent=4)
    except PermissionError:
        print("Error: Permission denied. Could not save to 'task.json'.")
    except Exception as error:
        print(f"An unexpected error occurred while saving: {error}")

def add_task(description):
    tasks = load_tasks()
    
    new_id = 1
    if tasks:
        new_id = max(task['id'] for task in tasks) + 1
        
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo", # Default status is always 'todo'
        "createdAt": now,
        "updatedAt": now
    }
    tasks.append(new_task)
    save_tasks(tasks)
    
    print(f"Task added successfully (ID: {new_id})")
    

def list_tasks(status_filter=None):
    

def main():
    if  len(sys.argv) < 2:
        print("Usage: task-cli [action] [arguments]")
        return
    
    action = sys.argv[1]
    
if __name__ == "__main__":
    main()