from typing import List
from backend.models.task import Task

def calculate_progress_for_tasks(tasks: List[Task]) -> float:
    """
    Calculate completion progress percentage from a list of tasks.
    Formula: (completed_tasks / total_tasks) * 100.0 rounded to 1 decimal place.
    If total_tasks == 0, returns 0.0.
    Status comparison is case-insensitive.
    """
    if not tasks:
        return 0.0
    total = len(tasks)
    completed = sum(1 for t in tasks if (t.status or "").strip().lower() == "completed")
    return round((completed / total) * 100.0, 1)
