from datetime import datetime
from manager import TaskManager


def print_menu():
    """
    Displays the main menu options to the user.
    """
    print("\nTask Manager Menu")
    print("1. Add Task")
    print("2. List All Tasks")
    print("3. Update Task")
    print("4. Mark Task as Completed")
    print("5. Delete Task")
    print("6. Exit")


def get_task_selection(tasks):
    """
    Displays a numbered list of tasks and prompts user to select one.

    Args:
        tasks (list): A list of Task objects.

    Returns:
        Task: The selected task object, or None if invalid input.
    """
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task.title} [{task.status}] (Due: {task.due_date})")
    choice = input("Select a task number: ")
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(tasks):
            return tasks[index]
    print("Invalid selection.")
    return None


def main():
    """
    The main entry point of the CLI-based Task Manager application.
    Handles user interaction and invokes appropriate task operations.
    """
    manager = TaskManager()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        # Add Task
        if choice == "1":
            try:
                title = input("Title: ").strip()
                if not title:
                    raise ValueError("Title cannot be empty.")

                description = input("Description: ").strip()

                due_date = input("Due Date (YYYY-MM-DD): ").strip()
                try:
                    if not due_date:
                        raise ValueError
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("Due date must be a valid date.")

                priority = input(
                    "Priority (Low/Medium/High): ").strip().capitalize()
                if priority not in ["Low", "Medium", "High"]:
                    raise ValueError("Priority must be Low, Medium, or High.")

                task = manager.add_task(title, description, due_date, priority)
                print(f"Task added.")

            except ValueError as ve:
                print(f"Input error: {ve}")
            except Exception as e:
                print(f"Failed to add task: {e}")

        # List Tasks with optional filtering
        elif choice == "2":
            try:
                filters = {}
                apply_filter = input(
                    "Would you like to apply a filter? (y/n): ").strip().lower()

                if apply_filter == "y":
                    print("Choose one filter only:")
                    print("1. Filter by status")
                    print("2. Filter by priority")
                    print("3. Filter by due date")

                    filter_choice = input("Enter choice (1-3): ").strip()

                    if filter_choice == "1":
                        status = input(
                            "Status (Pending/In Progress/Completed): ").strip().capitalize()
                        if status in ["Pending", "In progress", "Completed"]:
                            filters["status"] = status
                        else:
                            print("Invalid status. No filter applied.")

                    elif filter_choice == "2":
                        priority = input(
                            "Priority (Low/Medium/High): ").strip().capitalize()
                        if priority in ["Low", "Medium", "High"]:
                            filters["priority"] = priority
                        else:
                            print("Invalid priority. No filter applied.")

                    elif filter_choice == "3":
                        due_date = input("Due date (YYYY-MM-DD): ").strip()
                        try:
                            datetime.strptime(due_date, "%Y-%m-%d")
                            filters["due_date"] = due_date
                        except ValueError:
                            print("Invalid date format. No filter applied.")
                    else:
                        print("Invalid filter choice. No filter applied.")

                tasks = manager.list_tasks(filters if filters else None)

                if not tasks:
                    print("No tasks found.")
                else:
                    for task in tasks:
                        print("-" * 50)
                        print(task)

            except Exception as e:
                print(f"Failed to list tasks: {e}")

        # Update Task
        elif choice == "3":
            try:
                tasks = manager.list_tasks()
                if not tasks:
                    print("No tasks to update.")
                    continue

                task = get_task_selection(tasks)
                if task:
                    print("Leave blank to keep current value.")
                    new_title = input(f"New title: ") or task.title
                    new_desc = input(f"New description: ") or task.description
                    new_due = input(f"New due date: ") or task.due_date
                    new_priority = input(f"New priority: ") or task.priority
                    new_status = input(
                        "New status (Pending/In Progress/Completed): ").strip().capitalize() or task.status

                    if new_priority.capitalize() not in ["Low", "Medium", "High"]:
                        raise ValueError(
                            "Priority must be Low, Medium, or High.")
                    if new_priority not in ["Low", "Medium", "High"]:
                        raise ValueError(
                            "Priority must be Low, Medium, or High.")

                    # Validate status
                    if new_status not in ["Pending", "In progress", "Completed"]:
                        raise ValueError(
                            "Status must be Pending, In Progress, or Completed.")

                    # Validate due date
                    try:
                        datetime.strptime(new_due, "%Y-%m-%d")
                    except ValueError:
                        raise ValueError("Due date must be a valid date.")

                    updates = {
                        "title": new_title,
                        "description": new_desc,
                        "due_date": new_due,
                        "priority": new_priority.capitalize()
                    }

                    if manager.update_task(task.task_id, updates):
                        print("Task updated.")
                    else:
                        print("Update failed.")

            except ValueError as ve:
                print(f"Input error: {ve}")
            except Exception as e:
                print(f"Failed to update task: {e}")

        # Mark Task as Completed
        elif choice == "4":
            try:
                tasks = manager.list_tasks()
                if not tasks:
                    print("No tasks to mark as completed.")
                    continue

                task = get_task_selection(tasks)
                if task and manager.mark_completed(task.task_id):
                    print("Task marked as completed.")
                else:
                    print("Failed to mark task.")

            except Exception as e:
                print(f"Error during marking task: {e}")

        # Delete Task
        elif choice == "5":
            try:
                tasks = manager.list_tasks()
                if not tasks:
                    print("No tasks to delete.")
                    continue

                task = get_task_selection(tasks)
                if task and manager.delete_task(task.task_id):
                    print("Task deleted.")
                else:
                    print("Delete failed.")

            except Exception as e:
                print(f"Error during delete: {e}")

        # Exit
        elif choice == "6":
            print("Exiting Task Manager.")
            break

        else:
            print("Invalid choice. Please select a number from 1 to 6.")


if __name__ == "__main__":
    main()
