class Data():
    product_backlog_items = {
        "item1": {
            "task_name": "Task 1",
            "description": "Description 1",
            "priority": "Priority 1",
            "story_points": "Story Points 1",
            "tags": "Tags 1",
            "stage": "Stage 1",
            "assignee": "Assignee 1"
        },
        "item2": {
            "task_name": "Task 2",
            "description": "Description 2",
            "priority": "Priority 2",
            "story_points": "Story Points 2",
            "tags": "Tags 2",
            "stage": "Stage 2",
            "assignee": "Assignee 2"
        },
        "item3": {
            "task_name": "Task 3",
            "description": "Description 3",
            "priority": "Priority 3",
            "story_points": "Story Points 3",
            "tags": "Tags 3",
            "stage": "Stage 3",
            "assignee": "Assignee 3"
        },
    }

    def __init__(self):
        pass

    def get_product_backlog_items(self):
        return self.product_backlog_items
    
    def get_product_backlog_item(self, id):
        return self.product_backlog_items[id]

    def add_product_backlog_item(self, task_name, description, priority, story_points, tags, stage, assignee):
        item = {
            "task_name": task_name,
            "description": description,
            "priority": priority,
            "story_points": story_points,
            "tags": tags,
            "stage": stage,
            "assignee": assignee
        }
        self.product_backlog_items[f"item{len(self.product_backlog_items)+1}"] = item

    def remove_product_backlog_item(self, id):
        self.product_backlog_items.pop(id)

    def update_product_backlog_item(self, task_name, description="", priority="", story_points="", tags=[], stage="", assignee=[]):
        item = {
            "task_name": task_name,
            "description": description,
            "priority": priority,
            "story_points": story_points,
            "tags": tags,
            "stage": stage,
            "assignee": assignee
        }
        self.product_backlog_items[f"item{(self.product_backlog_items)+1}"] = item