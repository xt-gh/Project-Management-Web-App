from datetime import datetime
import time
import asyncio
from bson.objectid import ObjectId
from data.db import db

class UserData():
    collection_name = "user"
    collection = db[collection_name]

    async def ping(self):
        try:
            db.client.admin.command('ping')
            print("\033[42mDATABASE: Successfully connected to MongoDB\033[0m")
        except Exception as e:
            print(f"\031[42mAn error occurred: {e}\033[0m")

    # Method to get all users
    async def get_all_users(self):
        print("\033[42mDATABASE: Getting all users informations\033[0m")
        documents = list(self.collection.find({}))
        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        print("\033[42mDATABASE: User information fetched\033[0m")
        for item in documents:
            print(item)
        return documents
    
    async def get_all_usernames(self):
        print("\033[42mDATABASE: Getting all usernames\033[0m")
        documents = list(self.collection.find({}, {"username": 1}))
        usernames = []
        for item in documents:
            if 'username' in item:
                usernames.append(item['username'])
        print("\033[42mDATABASE: Usernames fetched\033[0m")
        print(usernames)
        return usernames
    
    # Method to get a single user by username
    async def get_user(self, username):
        print("\033[42mDATABASE: Getting user", username)
        document = self.collection.find_one({"username": username})
        if document:
            document['_id'] = str(document['_id'])
        print(document)
        print("\033[42mDATABASE: User information fetched\033[0m")
        return document
    
    # Method to add new user
    async def add_user(self, item):
        print("\033[42mDATABASE: Adding new user\033[0m")
        if '_id' in item:
            if isinstance(item['_id'], str) and ObjectId.is_valid(item['_id']):
                item['_id'] = ObjectId(item['_id'])
        result = self.collection.insert_one(item)
        print("\033[42mDATABASE: New user added\033[0m")
        return {"insertedId": str(result.inserted_id)}
    
    # Method to update a user information
    async def update_user_info(self, account_id, updated_fields):
        print("\033[42mDATABASE: Updating user info\033[0m", str(updated_fields))
        if '_id' in updated_fields:
            del updated_fields['_id']
        result = self.collection.update_one(
            {"_id": ObjectId(account_id)},
            {"$set": updated_fields}
        )
        return {
            "matchedCount": result.matched_count,
            "modifiedCount": result.modified_count
        }
    
    # Method to remove a user by its _id
    async def remove_user(self, user_id):
        print("\033[42mDATABASE: Removing user\033[0m", user_id)
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return {"deletedCount": result.deleted_count}
    
    async def get_user_by_id(self, user_id):
        print("\033[42mDATABASE: Getting user", user_id)
        document = self.collection.find_one({"_id": ObjectId(user_id)})
        if document:
            document['_id'] = str(document['_id'])
        print(document)
        print("\033[42mDATABASE: User information fetched\033[0m")
        return document

    
if __name__ == "__main__":
    data_api = UserData()

    def create_admin(name):

        admin = {
            "username": "name",
            "password": "password",
            "account_type": "admin"
        }
        asyncio.run(data_api.add_user(admin))

    def print_all_users():
        items = asyncio.run(data_api.get_all_users())
        for item in items:
            print(json.dumps(item, indent=4))

    # create_admin("admin")
    print_all_users()