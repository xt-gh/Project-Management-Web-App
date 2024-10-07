class TaskFilter():
    def filter_tasks(self, tasks, filter_tag):
        if filter_tag == "All Tasks":
            return tasks
        else:
            return list(filter(lambda item: filter_tag in item["tags"], tasks))