from pymongo import MongoClient
from datetime import datetime
import requests
import json

class Data():
    def __init__(self):
        self.base_url = 'https://ap-southeast-1.aws.data.mongodb-api.com/app/data-vevzgeu/endpoint/data/v1'
        self.api_key = 'oFUhaqY07FnEp8S3hU4Bw8bxTMHM4plR3kWxT1856Wt3Hc0iiUjcn3vrhzDzLoyK'  # Replace with your API key
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        self.database_name = "projectDatabase"
        self.collection_name = "task"
    
    
    product_backlog_items = {
        
        "item1": {
            "task_name": "Task 1",
            "description": "Description 1",
            "priority": "Low",
            "story_points": "1",
            "tags": ["Front-end", "UI"],
            "stage": "Planning",
            "status": "Not Started",
            "type": "User Story",
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
            "status": "Not Started",
            "type": "User Story",
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
            "status": "Not Started",
            "type": "User Story",
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
            "status": "Not Started",
            "type": "User Story",
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
            "status": "Not Started",
            "type": "User Story",
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
            "status": "Not Started",
            "type": "User Story",
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
            "status": "Not Started",
            "type": "User Story",
            "assignee": "John Smith",
            "logs": ["John Smith added this item on 2022-01-07 04:00 PM", "John Smith edited this item on 2022-01-08 05:00 PM"]
        }
    }

    # def __init__(self):
    #     pass

    # Method to get all product backlog items
    def get_product_backlog_items(self):
        url = f"{self.base_url}/action/find"
        payload = json.dumps({
            "dataSource": "helium",  # Replace with your data source name
            "database": self.database_name,
            "collection": self.collection_name,
        })
        response = requests.post(url, headers=self.headers, data=payload)
        # print(response.json())
        return response.json()['documents']

    # Method to get a single product backlog item by its _id
    def get_product_backlog_item(self, item_id):
        url = f"{self.base_url}/action/findOne"
        payload = json.dumps({
            "dataSource": "helium",  # Replace with your data source name
            "database": self.database_name,
            "collection": self.collection_name,
            "filter": {"_id": {"$oid": item_id}}
        })
        response = requests.post(url, headers=self.headers, data=payload)
        # print(response.json())
        return response.json()['document']

    # Method to add a new product backlog item
    def add_product_backlog_item(self, item):
        url = f"{self.base_url}/action/insertOne"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
            "document": item
        })
        response = requests.post(url, headers=self.headers, data=payload)
        return response.json()

    # Method to update a product backlog item
    def update_product_backlog_item(self, item_id, updated_fields):
        url = f"{self.base_url}/action/updateOne"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
            "filter": {"_id": {"$oid": item_id}},
            "update": {"$set": updated_fields}
        })
        response = requests.post(url, headers=self.headers, data=payload)
        return response.json()

    # Method to remove a product backlog item by its _id
    def remove_product_backlog_item(self, item_id):
        url = f"{self.base_url}/action/deleteOne"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
            "filter": {"_id": {"$oid": item_id}}
        })
        response = requests.post(url, headers=self.headers, data=payload)
        return response.json()

if __name__ == "__main__":
    data_api = Data()

    # Get all product backlog items
    items = data_api.get_product_backlog_items()
    for item in items:
        print(item)

    # Add a new product backlog item
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
    add_response = data_api.add_product_backlog_item(new_item)
    print("New Item Added:", add_response)

    # Get a specific product backlog item by ID
    first_item_id = items[0]['_id']  # Extract ObjectId from first item
    fetched_item = data_api.get_product_backlog_item(first_item_id)
    print("Fetched Item:", fetched_item)

    # Update an item
    updated_fields = {
        "status": "Completed",
        "logs": ["Item was marked as completed on 2022-02-01"]
    }
    update_response = data_api.update_product_backlog_item(first_item_id, updated_fields)
    print("Updated Item:", update_response)

    items = data_api.get_product_backlog_items()
    for item in items:
        print(item)

    # Remove an item
    remove_response = data_api.remove_product_backlog_item(first_item_id)
    print("Item Removed:", remove_response)
    items = data_api.get_product_backlog_items()
    for item in items:
        print(item)