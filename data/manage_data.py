class Data():
    product_backlog_items = {

        "item1": {
            "task_name": "Task 1",
            "description": "Description 1",
            "priority": "Low",
            "story_points": "1",
            "tags": ["Front-end", "UI"],
            "stage": "Planning",
            "assignee": ["John Doe"]
        },
        "item2": {
            "task_name": "Task 2",
            "description": "Description 2",
            "priority": "Medium",
            "story_points": "2",
            "tags": ["Back-end", "API"],
            "stage": "Development",
            "assignee": ["Jane Doe"]
        },
        "item3": {
            "task_name": "Task 3",
            "description": "Description 3",
            "priority": "Important",
            "story_points": "3",
            "tags": ["Database"],
            "stage": "Testing",
            "assignee": ["John Smith"]
        },
        "item4": {
            "task_name": "Task 4",
            "description": "Description 4",
            "priority": "Urgent",
            "story_points": "4",
            "tags": ["UI", "Testing"],
            "stage": "Implementation",
            "assignee": ["Jane Smith"]
        },
        "item5": {
            "task_name": "Task 5",
            "description": "Description 5",
            "priority": "Low",
            "story_points": "5",
            "tags": ["UX"],
            "stage": "Planning",
            "assignee": ["John Doe"]
        },
        "item6": {
            "task_name": "Task 6",
            "description": "Description 6",
            "priority": "Medium",
            "story_points": "6",
            "tags": ["Testing", "Framework"],
            "stage": "Development",
            "assignee": ["Jane Doe"]
        },
        "item7": {
            "task_name": "Task 7",
            "description": "Description 7",
            "priority": "Important",
            "story_points": "7",
            "tags": ["Front-end", "Back-end", "API"],
            "stage": "Testing",
            "assignee": ["John Smith"]
        }
    }

    def __init__(self):
        pass

    def get_product_backlog_items(self):
        return self.product_backlog_items
    
    def get_product_backlog_item(self, id):
        return self.product_backlog_items[id]

    def add_product_backlog_item(self, task_name, description, priority, story_points, tags, stage, assignee):
        item = {
            "id": f"{len(self.product_backlog_items)+1}",
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

    def update_product_backlog_item(self, id, task_name="", description="", priority="", story_points="", tags=[], stage="", assignee=[]):
        original_item = self.product_backlog_items[id]
        original_item.update({
            "task_name": task_name,
            "description": description,
            "priority": priority,
            "story_points": story_points,
            "tags": tags,
            "stage": stage,
            "assignee": assignee
        })