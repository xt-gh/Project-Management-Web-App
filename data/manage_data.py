import asyncio
from datetime import datetime
from bson.objectid import ObjectId
from data.db import db

class Data():
    collection_name = "task"
    collection = db[collection_name]
    
    product_backlog_items = [
        {
            "_id": "item1",
            "task_name": "Task 1",
            "description": "Description 1",
            "priority": "Low",
            "story_points": "1",
            "tags": ["Front-end", "UI"],
            "stage": "Planning",
            "status": "Not Started",
            "type": "User Story",
            "assignee": "John Doe",
            "admin_add_date": datetime.now().strftime("%d-%m-%Y"),
            "logs": ["John Doe added this item on 2022-01-01 10:00 AM", "John Doe edited this item on 2022-01-02 11:00 AM"]
        },
        {
            "_id": "item2",
            "task_name": "Task 2",
            "description": "Description 2",
            "priority": "Medium",
            "story_points": "2",
            "tags": ["Back-end", "API"],
            "stage": "Development",
            "status": "Not Started",
            "type": "User Story",
            "assignee": "Jane Doe",
            "admin_add_date": datetime.now().strftime("%d-%m-%Y"),
            "logs": ["Jane Doe added this item on 2022-01-02 11:00 AM", "Jane Doe edited this item on 2022-01-03 12:00 PM"]
        },
        {
            "_id": "item3",
            "task_name": "Task 3",
            "description": "Description 3",
            "priority": "Important",
            "story_points": "3",
            "tags": ["Database"],
            "stage": "Testing",
            "status": "Not Started",
            "type": "User Story",
            "assignee": "John Smith",
            "admin_add_date": datetime.now().strftime("%d-%m-%Y"),
            "logs": ["John Smith added this item on 2022-01-03 12:00 PM", "John Smith edited this item on 2022-01-04 01:00 PM"]
        },
        {
            "_id": "item4",
            "task_name": "Task 4",
            "description": "Description 4",
            "priority": "Urgent",
            "story_points": "5",
            "tags": ["UI", "Testing"],
            "stage": "Implementation",
            "status": "Not Started",
            "type": "User Story",
            "assignee": "Jane Smith",
            "admin_add_date": datetime.now().strftime("%d-%m-%Y"),
            "logs": ["Jane Smith added this item on 2022-01-04 01:00 PM", "Jane Smith edited this item on 2022-01-05 02:00 PM"]
        }
    ]
    
    async def ping(self):
        try:
            db.client.admin.command('ping')
            print("\033[42mDATABASE: Successfully connected to MongoDB\033[0m")
        except Exception as e:
            print(f"\031[42mAn error occurred: {e}\033[0m")
    
    # Method to get all product backlog items
    async def get_product_backlog_items(self):
        print("\033[42mDATABASE: Getting product backlog items\033[0m")
        documents = list(self.collection.find({}))
        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        print("\033[42mDATABASE: Product backlog items fetched\033[0m")
        return documents

    # Method to get a single product backlog item by its _id
    async def get_product_backlog_item(self, item_id):
        print("\033[42mDATABASE: Getting product backlog item", item_id)
        document = self.collection.find_one({"_id": ObjectId(item_id)})
        if document:
            document['_id'] = str(document['_id'])
        print(document)
        print("\033[42mDATABASE: Product backlog item fetched\033[0m")
        return document

    # Method to add a new product backlog item
    async def add_product_backlog_item(self, item):
        print("\033[42mDATABASE: Adding new product backlog item\033[0m")
        if '_id' in item:
            if isinstance(item['_id'], str) and ObjectId.is_valid(item['_id']):
                item['_id'] = ObjectId(item['_id'])
        result = self.collection.insert_one(item)
        print("\033[42mDATABASE: New product backlog item added\033[0m")
        return {"insertedId": str(result.inserted_id)}

    # Method to update a product backlog item
    async def update_product_backlog_item(self, item_id, updated_fields):
        print("\033[42mDATABASE: Updating product backlog item\033[0m", str(updated_fields))
        if '_id' in updated_fields:
            del updated_fields['_id']
        result = self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": updated_fields}
        )
        return {
            "matchedCount": result.matched_count,
            "modifiedCount": result.modified_count
        }

    # Method to remove a product backlog item by its _id
    async def remove_product_backlog_item(self, item_id):
        print("\033[42mDATABASE: Removing product backlog item\033[0m", item_id)
        result = self.collection.delete_one({"_id": ObjectId(item_id)})
        return {"deletedCount": result.deleted_count}
    
    # Method to get all items from a sprint
    async def get_tasks_from_sprint_id(self, sprint_id):
        print("\033[42mDATABASE: Getting tasks from sprint ID", sprint_id, "\033[0m")
        documents = list(self.collection.find({"sprint_id": sprint_id}))
        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        print("\033[42mDATABASE: Sprint task items fetched\033[0m")
        return documents
    
    async def get_tasks_with_username(self, username):
        print("\033[42mDATABASE: Getting tasks with username", username, "\033[0m")
        documents = list(self.collection.find({"assignee": username}))
        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        print("\033[42mDATABASE: Tasks with username fetched\033[0m")
        return documents

if __name__ == "__main__":
    def print_all_items():
        items = asyncio.run(Data().get_product_backlog_items())
        for item in items:
            print(json.dumps(item, indent=4))

    def delete_all_items():
        items = asyncio.run(Data().get_product_backlog_items())
        for item in items:
            asyncio.run(Data().remove_product_backlog_item(item['_id']))

    def add_item():
        new_item = {
            "task_name": "New Task",
            "description": "New Task Description",
            "priority": "High",
            "story_points": 5,
            "tags": ["API", "Front-end"],
            "stage": "Development",
            "status": "In Progress",
            "type": "Bug",
            "assignee": "John Doe",
            "admin_add_date": datetime.utcnow().isoformat(),
            "logs": ["John Doe added this item on 2022-01-08 10:00 AM"]
        }
        asyncio.run(Data().add_product_backlog_item(new_item))

    def print_tasks_from_sprint_id(sprint_id):
        tasks = asyncio.run(Data().get_tasks_from_sprint_id(sprint_id))
        for task in tasks:
            print(json.dumps(task, indent=4))

    delete_all_items()