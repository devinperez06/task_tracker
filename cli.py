import argparse
import json
import datetime

# All methods are built with edge-cases in mind. For example, if you are trying to 
# delete a task with no tasks available to delete, you will receive a special message. 
# If you try to change the status of a task to the status that it already has, you will 
# receive a special message etc.

def read_from_json(file_path): # reads from data.json; returns an empty list if data.json is not in list format
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                print("Resetting JSON structure to an empty list...")
                return []
    except FileNotFoundError:
        return []

def write_to_json(file_path, data): # writes to data.json in correct format
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def find_task_by_id(tasks, task_id): # returns task with requested task id
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

def add(args): # adds a task to data.json with requested description; each task has an id, description, status, createdAt time, and updatedAt time
    tasks = read_from_json(file_path)
    count = len(tasks) + 1
    task = {
                'id': count, 
                'description': args.task, 
                'status': 'todo', 
                'createdAt': now.isoformat(), 
                'updatedAt': None
            }
    tasks.append(task)
    write_to_json(file_path, tasks)
    print("Task added successfully.")

def update(args): # updates a task with new requested description; updates updatedAt time
    tasks = read_from_json(file_path)
    if len(tasks) == 0:
        print("No tasks available to update. Add task(s) first.")
        return
    
    task = find_task_by_id(tasks, args.id)
    if not task:
        print(f"Task ID {args.id} not found.")
        return
    
    task['description'] = args.task
    task['updatedAt'] = now.isoformat()
    write_to_json(file_path, tasks)
    print(f"Task ID {args.id} updated successfully!")

def delete(args): # deletes a task from data.json with requested id; id numbers for all tasks are changed to maintain sequential order
    tasks = read_from_json(file_path)
    if len(tasks) == 0:
        print("No tasks available to delete. Add task(s) first.")
        return
    
    task = find_task_by_id(tasks, args.id)
    if not task:
        print(f"Task ID {args.id} not found.")
        return
    
    tasks.remove(task)
    for idx, task in enumerate(tasks):
        task['id'] = idx + 1

    write_to_json(file_path, tasks)
    print(f"Task ID {args.id} deleted successfully!")

def mark_in_progress(args): # marks a task with status: in-progress if task is not already in-progress
    tasks = read_from_json(file_path)
    if len(tasks) == 0:
        print("No tasks available to mark. Add task(s) first.")
        return
    
    task = find_task_by_id(tasks, args.id)
    if not task:
        print(f"Task ID {args.id} not found.")
        return

    if task['status'] == "in-progress":
        print("Task already in progress.")
        return
    
    task['status'] = "in-progress"
    task['updatedAt'] = now.isoformat()
    write_to_json(file_path, tasks)
    print(f"Task ID {args.id} status changed successfully!")

def mark_done(args): # marks a task with status: done if task is not already done
    tasks = read_from_json(file_path)
    if len(tasks) == 0:
        print("No tasks available to mark. Add task(s) first.")
        return
    
    task = find_task_by_id(tasks, args.id)
    if not task:
        print(f"Task ID {args.id} not found.")
        return

    if task['status'] == "done":
        print("Task already marked as done.")
        return
    
    task['status'] = "done"
    task['updatedAt'] = now.isoformat()
    write_to_json(file_path, tasks)
    print(f"Task ID {args.id} status changed successfully!")

def list_tasks(args): # lists all tasks with requested status
    tasks = read_from_json(file_path)
    filtered_tasks = [task['description'] for task in tasks if task['status'] == args.status]

    if not filtered_tasks:
        print("There are no tasks available with this status.")
        return
    
    print("\n".join(filtered_tasks))

def list_all(args): # lists all tasks from data.json
    tasks = read_from_json(file_path)
    if not tasks:
        print("No tasks available to list.")
        return
    
    print("\n".join(task['description'] for task in tasks))

def main(): # instantiates all necessary subparsers to be used in command-line
    global now
    now = datetime.datetime.now()

    parser = argparse.ArgumentParser(description="CLI application")
    subparsers = parser.add_subparsers(title="task-cli", dest="command")

    addtask_parser = subparsers.add_parser("add", help="Add a task.")
    addtask_parser.add_argument("task", help="The description of the task to be added.")
    addtask_parser.set_defaults(func=add)

    updatetask_parser = subparsers.add_parser("update", help="Update a task description by id.")
    updatetask_parser.add_argument("id", type=int, help="The id of the task to be updated.")
    updatetask_parser.add_argument("task", help="The new description of the task.")
    updatetask_parser.set_defaults(func=update)

    deletetask_parser = subparsers.add_parser("delete", help="Delete a task by id.")
    deletetask_parser.add_argument("id", type=int, help="The id of the task to be deleted.")
    deletetask_parser.set_defaults(func=delete)

    markinprogress_parser = subparsers.add_parser("mark-in-progress", help="Mark a task as 'in progress'.")
    markinprogress_parser.add_argument("id", type=int, help="The id of the task to be marked.")
    markinprogress_parser.set_defaults(func=mark_in_progress)

    markdone_parser = subparsers.add_parser("mark-done", help="Mark a task as done.")
    markdone_parser.add_argument("id", type=int, help="The id of the task to be marked.")
    markdone_parser.set_defaults(func=mark_done)

    list_parser = subparsers.add_parser("list", help="List all tasks by their status.")
    list_parser.add_argument("status", help="The status of the tasks to be listed.")
    list_parser.set_defaults(func=list_tasks)

    listall_parser = subparsers.add_parser("list-all", help="List all tasks.")
    listall_parser.set_defaults(func=list_all)

    args = parser.parse_args()

    if args.command:
        args.func(args)

file_path = 'data.json'

if __name__ == "__main__":
    main()