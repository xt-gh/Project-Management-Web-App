class TaskSorter():
    def priority_value(self, priority):
        priorities = [None, "Low", "Medium", "Important", "Urgent"]
        priority_level = priorities.index(priority) + 1
        return priority_level
    
    def sort_tasks(self, tasks, sort_label):
        if sort_label == "High to Low Priority":
            tasks.sort(key=lambda item: self.priority_value(item["priority"]), reverse=True)
        elif sort_label == "Low to High Priority":
            tasks.sort(key=lambda item: self.priority_value(item["priority"]), reverse=False)
        elif sort_label == "Oldest to Newest":
            tasks.sort(key=lambda item: item["admin_add_date"], reverse=False)
        elif sort_label == "Newest to Oldest":
            tasks.sort(key=lambda item: item["admin_add_date"], reverse=True)
        
        return tasks