from pymongo import MongoClient

class Data():
    # def __init__(self, uri='mongodb+srv://mwon0072:AVsCzA9IbIECXMNX@helium.6iy1m.mongodb.net/', database_name='projectDatabase', collection_name='task'):
    #     self.client = MongoClient(uri)
    #     self.db = self.client[database_name]
    #     self.collection = self.db[collection_name]
    
    
    product_backlog_items = {
        
        "item1": {
            "task_name": "Task 1",
            "description": "Description 1",
            "priority": "Low",
            "story_points": "1",
            "tags": ["Front-end", "UI"],
            "stage": "Planning",
            "assignee": "John Doe",
            "logs": ["John Doe added this item on 2022-01-01 10:00 AM", "John Doe edited this item on 2022-01-02 11:00 AM"]
        },
        "item2": {
            "task_name": "Task 2",
            "description": "Description 2",
            "priority": "Medium",
            "story_points": "2",
            "tags": ["Back-end", "API"],
            "stage": "Development",
            "assignee": "Jane Doe",
            "logs": ["Jane Doe added this item on 2022-01-02 11:00 AM", "Jane Doe edited this item on 2022-01-03 12:00 PM"]
        },
        "item3": {
            "task_name": "Task 3",
            "description": "Description 3",
            "priority": "Important",
            "story_points": "3",
            "tags": ["Database"],
            "stage": "Testing",
            "assignee": "John Smith",
            "logs": ["John Smith added this item on 2022-01-03 12:00 PM", "John Smith edited this item on 2022-01-04 01:00 PM"]
        },
        "item4": {
            "task_name": "Task 4",
            "description": "Description 4",
            "priority": "Urgent",
            "story_points": "5",
            "tags": ["UI", "Testing"],
            "stage": "Implementation",
            "assignee": "Jane Smith",
            "logs": ["Jane Smith added this item on 2022-01-04 01:00 PM", "Jane Smith edited this item on 2022-01-05 02:00 PM"]
        },
        "item5": {
            "task_name": "Task 5",
            "description": "Description 5",
            "priority": "Low",
            "story_points": "8",
            "tags": ["UX"],
            "stage": "Planning",
            "assignee": "John Doe",
            "logs": ["John Doe added this item on 2022-01-05 02:00 PM", "John Doe edited this item on 2022-01-06 03:00 PM"]
        },
        "item6": {
            "task_name": "Task 6",
            "description": "Description 6",
            "priority": "Medium",
            "story_points": "13",
            "tags": ["Testing", "Framework"],
            "stage": "Development",
            "assignee": "Jane Doe",
            "logs": ["Jane Doe added this item on 2022-01-06 03:00 PM", "Jane Doe edited this item on 2022-01-07 04:00 PM"]
        },
        "item7": {
            "task_name": "Task 7",
            "description": "Description 7",
            "priority": "Important",
            "story_points": "20",
            "tags": ["Front-end", "Back-end", "API"],
            "stage": "Testing",
            "assignee": "John Smith",
            "logs": ["John Smith added this item on 2022-01-07 04:00 PM", "John Smith edited this item on 2022-01-08 05:00 PM"]
        }
    }

    # def __init__(self):
    #     pass

    def get_product_backlog_items(self):
        return self.product_backlog_items
        # return self.collection.find()
    
    def get_product_backlog_item(self, id):
        return self.product_backlog_items[id]
        # return self.collection.find_one({"_id": id})

    def add_product_backlog_item(self, item):
        item = {
            "task_name": item["task_name"],
            "description": item["description"],
            "priority": item["priority"],
            "story_points": item["story_points"],
            "tags": item["tags"],
            "stage": item["stage"],
            "assignee": item["assignee"]
        }
        self.collection.insert_one(item)

    def remove_product_backlog_item(self, id):
        self.collection.delete_one({"_id": id})

    def update_product_backlog_item(self, id, item):
        self.collection.update_one({
            "task_name": item["task_name"],
            "description": item["description"],
            "priority": item["priority"],
            "story_points": item["story_points"],
            "tags": item["tags"],
            "stage": item["stage"],
            "assignee": item["assignee"]
        })

# data = Data()
# items = data.get_product_backlog_items()
# ids = []
# for item in items:
#     print(item)
#     ids.append(item["_id"])

# print()
# print(data.get_product_backlog_item(ids[-1]))