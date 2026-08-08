from datetime import datetime
import time
import asyncio
from bson.objectid import ObjectId
from data.db import db

class SprintData():
    collection_name = "sprint"
    collection = db[collection_name]

    sprint_board_items = [
        {
            "sprint_name": "Sprint1",
            "role_1": "Product_Owner",
            "role_2": "Scrum_Master",
            "team_members": ["John Doe", "John Smith"],
            "start_date": "2022-01-03",
            "end_date": "2022-02-03",
        },
        {
            "sprint_name": "Sprint2",
            "role_1": "Product_Owner",
            "role_2": "Scrum_Master",
            "team_members": ["Harry Smith", "John Smith"],
            "start_date": "2022-04-02",
            "end_date": "2022-05-03",
        }]
    
    async def ping(self):
        try:
            db.client.admin.command('ping')
            print("\033[42mDATABASE: Successfully connected to MongoDB\033[0m")
        except Exception as e:
            print(f"\031[42mAn error occurred: {e}\033[0m")
    
    # Method to get all sprint items
    async def get_sprint_items(self):
        print("\033[42mDATABASE: Getting sprint items\033[0m")
        documents = list(self.collection.find({}))
        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        print("\033[42mDATABASE: Sprint items fetched\033[0m")
        for item in documents:
            print(item)
        return documents

     # Method to add a new sprint
    async def add_sprint_item(self, item):
        print("\033[42mDATABASE: Adding new sprint\033[0m")
        if '_id' in item:
            if isinstance(item['_id'], str) and ObjectId.is_valid(item['_id']):
                item['_id'] = ObjectId(item['_id'])
        result = self.collection.insert_one(item)
        print("\033[42mDATABASE: New sprint added\033[0m")
        return {"insertedId": str(result.inserted_id)}
    
    # Method to update a sprint
    async def update_sprint_item(self, sprint_id, updated_fields):
        print("\033[42mDATABASE: Updating sprint\033[0m")
        print(sprint_id)
        print(updated_fields)
        if '_id' in updated_fields:
            del updated_fields['_id']
        result = self.collection.update_one(
            {"_id": ObjectId(sprint_id)},
            {"$set": updated_fields}
        )
        print("\033[42mDATABASE: Sprints fetched\033[0m")
        return {
            "matchedCount": result.matched_count,
            "modifiedCount": result.modified_count
        }

    # Method to delete a sprint
    async def remove_sprint_item(self, sprint_id):
        print("\033[42mDATABASE: Removing sprint\033[0m")
        result = self.collection.delete_one({"_id": ObjectId(sprint_id)})
        print("\033[42mDATABASE: Sprint deleted\033[0m")
        return {"deletedCount": result.deleted_count}
    
    # Method to get a single sprint by its _id
    async def get_sprint_item(self, item_id):
        print("\033[42mDATABASE: Getting sprint", item_id)
        document = self.collection.find_one({"_id": ObjectId(item_id)})
        if document:
            document['_id'] = str(document['_id'])
        print(document)
        print("\033[42mDATABASE: Sprint fetched\033[0m")
        return document

# SPRINTS =  asyncio.run(SprintData().get_sprint_items())
# for sprint in SPRINTS:
#     print(sprint)
#     asyncio.run(SprintData().remove_sprint_item(sprint['_id']))

    
if __name__ == "__main__":
    data_api = SprintData()

    async def main():
        # Get all sprints
        items = await data_api.get_sprint_items()  # Await the async function
        for item in items:
            print(json.dumps(item, indent=4))

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
        # first_item_id = items[0]['_id']  # Extract ObjectId from first item
        # fetched_item = await data_api.get_sprint_item(first_item_id)
        # fetched_item['start_date'] = "01-10-2024"
        # del fetched_item['_id']
        # response = await data_api.update_sprint_item(sprint_id=first_item_id, updated_fields=fetched_item)
        # print("DATABASE: Updated Item:", response)

        # print("DATABASE: Fetched Item:", await data_api.get_sprint_item(first_item_id))
