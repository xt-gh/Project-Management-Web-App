from datetime import datetime
import time
import requests
import json

class Data():
    base_url = 'https://ap-southeast-1.aws.data.mongodb-api.com/app/data-vevzgeu/endpoint/data/v1'
    api_key = 'oFUhaqY07FnEp8S3hU4Bw8bxTMHM4plR3kWxT1856Wt3Hc0iiUjcn3vrhzDzLoyK'  # Replace with your API key
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }
    database_name = "projectDatabase"
    collection_name = "task"
    
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
            "admin_add_date": datetime.utcnow().isoformat(),
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
            "admin_add_date": datetime.utcnow().isoformat(),
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
            "admin_add_date": datetime.utcnow().isoformat(),
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
            "admin_add_date": datetime.utcnow().isoformat(),
            "logs": ["Jane Smith added this item on 2022-01-04 01:00 PM", "Jane Smith edited this item on 2022-01-05 02:00 PM"]
        }
    ]
    
    async def ping(self):
        try:
            url = f"{self.base_url}/action/findOne"
            payload = json.dumps({
                "dataSource": "helium",  # Replace with your data source name
                "database": self.database_name,
                "collection": self.collection_name,
                "filter": {}
            })
            response = requests.post(url, headers=self.headers, data=payload)
            if response.status_code == 200:
                print("\033[42mDATABASE: Successfully connected to MongoDB\033[0m")
            else:
                print(f"\031[42mFailed to connect to MongoDB: {response.status_code}\033[0m")
        except Exception as e:
            print(f"\031[42mAn error occurred: {e}\033[0m")
    
    # Method to get all product backlog items
    async def get_product_backlog_items(self):
        # time.sleep(1)
        # return self.product_backlog_items
        print("\033[42mDATABASE: Getting product backlog items\033[0m")
        url = f"{self.base_url}/action/find"
        payload = json.dumps({
            "dataSource": "helium",  # Replace with your data source name
            "database": self.database_name,
            "collection": self.collection_name,
        })
        response = requests.post(url, headers=self.headers, data=payload)
        # print(response.json())
        print("\033[42mDATABASE: Product backlog items fetched\033[0m")
        return response.json()['documents']

    # Method to get a single product backlog item by its _id
    async def get_product_backlog_item(self, item_id):
        # for item in self.product_backlog_items:
        #     if item['_id'] == item_id:
        #         return item
        
        print("\033[42mDATABASE: Getting product backlog item", item_id)
        url = f"{self.base_url}/action/findOne"
        payload = json.dumps({
            "dataSource": "helium",  # Replace with your data source name
            "database": self.database_name,
            "collection": self.collection_name,
            "filter": {"_id": {"$oid": item_id}}
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print(response.json())
        print("\033[42mDATABASE: Product backlog item fetched\033[0m")
        return response.json()['document']

    # Method to add a new product backlog item
    async def add_product_backlog_item(self, item):
        # item['_id'] = f"item{len(self.product_backlog_items) + 1}"
        # self.product_backlog_items.append(item)
        print("\033[42mDATABASE: Adding new product backlog item\033[0m")
        url = f"{self.base_url}/action/insertOne"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
            "document": item
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print("\033[42mDATABASE: New product backlog item added\033[0m")
        return response.json()

    # Method to update a product backlog item
    async def update_product_backlog_item(self, item_id, updated_fields):
        # for item in self.product_backlog_items:
        #     if item['_id'] == item_id:
        #         for key, value in updated_fields.items():
        #             item[key] = value
                # return item
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
    async def remove_product_backlog_item(self, item_id):
        # for i, item in enumerate(self.product_backlog_items):
        #     if item['_id'] == item_id:
        #         self.product_backlog_items.pop(i)
                # return item
        print("\033[42mDATABASE: Removing product backlog item", item_id)
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
    print("DATABASE: New Item Added:", add_response)

    # Get a specific product backlog item by ID
    first_item_id = items[0]['_id']  # Extract ObjectId from first item
    fetched_item = data_api.get_product_backlog_item(first_item_id)
    print("DATABASE: Fetched Item:", fetched_item)

    # Update an item
    updated_fields = {
        "status": "Completed",
        "logs": ["Item was marked as completed on 2022-02-01"]
    }
    update_response = data_api.update_product_backlog_item(first_item_id, updated_fields)
    print("DATABASE: Updated Item:", update_response)

    items = data_api.get_product_backlog_items()
    for item in items:
        print(item)

    # Remove an item
    remove_response = data_api.remove_product_backlog_item(first_item_id)
    print("DATABASE: Item Removed:", remove_response)
    items = data_api.get_product_backlog_items()
    for item in items:
        print(item)