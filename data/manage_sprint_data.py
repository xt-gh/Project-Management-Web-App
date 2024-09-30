from datetime import datetime
import time
import requests
import json
import asyncio

class SprintData():
    base_url = 'https://ap-southeast-1.aws.data.mongodb-api.com/app/data-vevzgeu/endpoint/data/v1'
    api_key = 'oFUhaqY07FnEp8S3hU4Bw8bxTMHM4plR3kWxT1856Wt3Hc0iiUjcn3vrhzDzLoyK'  
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }
    database_name = "projectDatabase"
    collection_name = "sprint"

    sprint_board_items = [
        {
            "sprint_name": "Sprint1",
            "role_1": "Product_Owner",
            "role_2": "Scrum_Master",
            "team_members": ["John Doe", "John Smith"],
            "start_date": "2022-01-03",
            "end_date": "2022-02-03",
            "status": "In Progress"
        },
        {
            "sprint_name": "Sprint2",
            "role_1": "Product_Owner",
            "role_2": "Scrum_Master",
            "team_members": ["Harry Smith", "John Smith"],
            "start_date": "2022-04-02",
            "end_date": "2022-05-03",
            "status": "Not Started"
        }]
    
    async def ping(self):
        try:
            url = f"{self.base_url}/action/findOne"
            payload = json.dumps({
                "dataSource": "helium",
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
    
    # Method to get all sprint items
    async def get_sprint_items(self):
        print("\033[42mDATABASE: Getting sprint items\033[0m")
        url = f"{self.base_url}/action/find"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print("\033[42mDATABASE: Sprint items fetched\033[0m")
        for item in response.json()['documents']:
            print(item)
        return response.json()['documents']

     # Method to add a new sprint
    async def add_sprint_item(self, item):
        print("\033[42mDATABASE: Adding new sprint\033[0m")
        url = f"{self.base_url}/action/insertOne"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
            "document": item
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print("\033[42mDATABASE: New sprint added\033[0m")
        return response.json()
    
    # Method to update a sprint
    async def update_sprint_item(self, sprint_id, updated_fields):
        print("\033[42mDATABASE: Updating sprint\033[0m")
        print(sprint_id)
        print(updated_fields)
        url = f"{self.base_url}/action/updateOne"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
        })
        response = requests.post(url, headers=self.headers, data=payload)
        # print(response.json())
        print("\033[42mDATABASE: Sprints fetched\033[0m")
        return response.json()['documents']
    
    # Method to get a single sprint by its _id
    async def get_sprint_item(self, item_id):
        print("\033[42mDATABASE: Getting sprint", item_id)
        url = f"{self.base_url}/action/findOne"
        payload = json.dumps({
            "dataSource": "helium",  # Replace with your data source name
            "database": self.database_name,
            "collection": self.collection_name,
            "filter": {"_id": {"$oid": item_id}}
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print(response.json())
        print("\033[42mDATABASE: Sprint deleted\033[0m")
        return response.json()

    # Method to delete a sprint
    async def remove_sprint_item(self, sprint_id):
        print("\033[42mDATABASE: Removing sprint\033[0m")
        url = f"{self.base_url}/action/deleteOne"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
            "filter": {"_id": {"$oid": sprint_id}}
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print(response.json())
        print("\033[42mDATABASE: Sprint deleted\033[0m")
        return response.json()
    
    # Method to get a single sprint by its _id
    async def get_sprint_item(self, item_id):
        print("\033[42mDATABASE: Getting sprint", item_id)
        url = f"{self.base_url}/action/findOne"
        payload = json.dumps({
            "dataSource": "helium",  # Replace with your data source name
            "database": self.database_name,
            "collection": self.collection_name,
            "filter": {"_id": {"$oid": item_id}}
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print(response.json()['document'])
        print("\033[42mDATABASE: Sprint fetched\033[0m")
        return response.json()['document']

# SPRINTS =  asyncio.run(SprintData().get_sprint_items())
# for sprint in SPRINTS:
#     print(sprint)
#     asyncio.run(SprintData().remove_sprint_item(sprint['_id']))

    
if __name__ == "__main__":
    data_api = SprintData()

    async def main():
        # Get all sprints
        items = await data_api.get_sprint_items()  # Await the async function
        # for item in items:
        #     print(item)

        # # Add a new sprint
        # new_item = {
        #     "sprint_name":"Sprint 5",
        #     "start_date":"2024-09-27T10:00:00Z",
        #     "end_date":"2024-10-10T10:00:00Z",
        #     "status":"In progress",
        #     "Asignee":["Aiyowei","Minyee"]
        # }
        # add_response = await data_api.add_sprint_item(new_item)
        # print("DATABASE: New Item Added:", add_response)

        # Get a specific sprint by ID
        first_item_id = items[0]['_id']  # Extract ObjectId from first item
        fetched_item = await data_api.get_sprint_item(first_item_id)
        fetched_item['sprint_name'] = "Completed"
        await data_api.update_sprint_item(first_item_id, fetched_item)


        print("DATABASE: Fetched Item:", await data_api.get_sprint_item(first_item_id))

    asyncio.run(main())