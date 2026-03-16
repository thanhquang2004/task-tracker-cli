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
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks found. Your to-do list is empty!")
        return

    if status_filter:
        filtered_tasks = [t for t in tasks if t['status'] == status_filter]
        if not filtered_tasks:
            print(f"No tasks found with status: {status_filter}")
            return    
    else:
        filtered_tasks = tasks
    
    print(f"{'ID':<5} | {'Status':<15} | {'Description'}")
    print("-" * 40)
    for task in filtered_tasks:
        print(f"{task['id']:<5} | {task['status']:<15} | {task['description']}")

def update_task(task_id, new_description):
    tasks = load_tasks()
    
    task_found=False
    
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task_found=True
            break
    
    if task_found:
        save_tasks(tasks)
        print(f"Task {task_id} updated successfully.")
    else:
        print(f"Error: Task with ID {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    original_count = len(tasks)
    
    tasks = [t for t in tasks if t['id'] != task_id]
    
    if len(tasks) < original_count:
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Error: Task with ID {task_id} not found.")

def change_status(task_id, new_status):
    tasks=load_tasks()
    
    task_found = False
    
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status
            task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task_found = True
            break
    
    if task_found:
        save_tasks(tasks)
        print(f"Task {task_id} updated successfully.")
    else:
        print(f"Error: Task with ID {task_id} not found.")

def main():
    if  len(sys.argv) < 2:
        print("Usage: task-cli [action] [arguments]")
        return
    
    command = sys.argv[1].lower()
    
    if command == "add" and len(sys.argv) > 2:
        add_task(sys.argv[2])
    elif command == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status)
    elif command == "update" and len(sys.argv) > 3:
        task_id = int(sys.argv[2])
        new_desc = sys.argv[3]
        update_task(task_id, new_desc)
    elif command == "delete" and len(sys.argv) > 2:
        task_id = int(sys.argv[2])
        delete_task(task_id)
    elif command == "mark-in-progress" and len(sys.argv) > 2:
        task_id = int(sys.argv[2])
        change_status(task_id, "in-progress")
    elif command == "mark-done" and len(sys.argv) > 2:
        task_id = int(sys.argv[2])
        change_status(task_id, "done")
    else:
        print("Invalid command or missing arguments.")
    
if __name__ == "__main__":
    main()