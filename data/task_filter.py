class TaskFilter():
    def filter_task(self, tasks, filter_tags):
        """Filter tasks based on a list of selected tags."""
        if not filter_tags or "All Tasks" in filter_tags:
            return tasks  # Return all items if no filter is applied
        else:
            filtered_tasks = []
            # Loop through each task
            for task in tasks:
                # Check if all selected tags are present in the task's tags
                if all(tag in task["tags"] for tag in filter_tags):
                    filtered_tasks.append(task)
            return filtered_tasks