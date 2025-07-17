from task import Task
from pymongo import MongoClient


class TaskManager:
    """
    Manages CRUD operations for tasks using a MongoDB backend.

    Attributes:
        client (MongoClient): Connection to the MongoDB server.
        db (Database): The task database instance.
        collection (Collection): The MongoDB collection for storing tasks.
    """

    def __init__(self):
        """
        Initializes the TaskManager, connects to MongoDB,
        and ensures a unique index on 'task_id'.
        """
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client["task_db"]
        self.collection = self.db["tasks"]
        self.collection.create_index("task_id", unique=True)

    def add_task(self, title, description, due_date, priority):
        """
        Creates and inserts a new task into the database.

        Args:
            title (str): Task title.
            description (str): Task description.
            due_date (str): Due date in 'YYYY-MM-DD' format.
            priority (str): Priority level (Low, Medium, High).

        Returns:
            Task: The newly created Task object.
        """
        task = Task(title, description, due_date, priority)
        self.collection.insert_one(task.to_dict())
        return task

    def list_tasks(self, filters=None):
        """
        Retrieves tasks from the database with optional filtering.

        Args:
            filters (dict, optional): MongoDB query filters.

        Returns:
            list: A list of Task objects matching the filter.
        """
        filters = filters or {}
        documents = self.collection.find(filters)
        tasks = []
        for doc in documents:
            task = Task(
                title=doc['title'],
                description=doc['description'],
                due_date=doc['due_date'],
                priority=doc['priority'],
            )
            task.task_id = doc['task_id']
            task.status = doc.get('status', 'Pending')
            task.created_at = doc.get('created_at')
            tasks.append(task)
        return tasks

    def update_task(self, task_id, updates):
        """
        Updates fields of an existing task.

        Args:
            task_id (str): The unique ID of the task.
            updates (dict): Dictionary of fields to update.

        Returns:
            bool: True if a task was modified, False otherwise.
        """
        result = self.collection.update_one(
            {"task_id": task_id},
            {"$set": updates}
        )
        return result.modified_count > 0

    def mark_completed(self, task_id):
        """
        Marks the specified task as completed.

        Args:
            task_id (str): The task ID to mark as completed.

        Returns:
            bool: True if the task was updated, False otherwise.
        """
        return self.update_task(task_id, {"status": "Completed"})

    def delete_task(self, task_id):
        """
        Deletes a task from the database.

        Args:
            task_id (str): The ID of the task to delete.

        Returns:
            bool: True if a task was deleted, False otherwise.
        """
        result = self.collection.delete_one({"task_id": task_id})
        return result.deleted_count > 0
