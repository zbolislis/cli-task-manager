import uuid
from datetime import datetime


class Task:
    """
    Represents a task in the task management system.

    Attributes:
        task_id (str): Unique identifier for the task.
        title (str): Title or name of the task.
        description (str): Detailed description of the task.
        due_date (str): Due date for task completion (format: YYYY-MM-DD).
        priority (str): Priority level (Low, Medium, High).
        status (str): Current status of the task (default: 'Pending').
        created_at (datetime): Timestamp of task creation.
    """

    def __init__(self, title, description, due_date, priority):
        """
        Initializes a new Task instance.

        Args:
            title (str): Title of the task.
            description (str): Description of the task.
            due_date (str): Due date for the task.
            priority (str): Priority level (Low, Medium, High).
        """

        self.task_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.due_date = due_date  # Expecting string or datetime
        self.priority = priority  # Low / Medium / High
        self.status = 'Pending'
        self.created_at = datetime.now()

    def to_dict(self):
        """
        Converts the Task object to a dictionary format suitable for database storage.

        Returns:
            dict: Dictionary representation of the task.
        """

        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at
        }

    def __str__(self):
        """
        Returns a human-readable string representation of the task.

        Returns:
            str: Formatted string containing task details.
        """
        return f"[{self.status}] {self.title} ({self.priority}) - Due: {self.due_date}"
