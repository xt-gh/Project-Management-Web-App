from datetime import datetime
import time
import requests
import json
import asyncio

class UserData():
    base_url = 'https://ap-southeast-1.aws.data.mongodb-api.com/app/data-vevzgeu/endpoint/data/v1'
    api_key = 'oFUhaqY07FnEp8S3hU4Bw8bxTMHM4plR3kWxT1856Wt3Hc0iiUjcn3vrhzDzLoyK'  
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }
    database_name = "projectDatabase"
    collection_name = "user"

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

    # Method to get all users
    async def get_all_users(self):
        print("\033[42mDATABASE: Getting all users informations\033[0m")
        url = f"{self.base_url}/action/find"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print("\033[42mDATABASE: User information fetched\033[0m")
        for item in response.json()['documents']:
            print(item)
        return response.json()['documents']
    
    async def get_all_usernames(self):
        print("\033[42mDATABASE: Getting all usernames\033[0m")
        url = f"{self.base_url}/action/find"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print("\033[42mDATABASE: Usernames fetched\033[0m")
        usernames = [item['username'] for item in response.json()['documents']]
        print(usernames)
        return usernames
    
    # Method to get a single user by username
    async def get_user(self, username):
        print("\033[42mDATABASE: Getting user", username)
        url = f"{self.base_url}/action/findOne"
        payload = json.dumps({
            "dataSource": "helium", 
            "database": self.database_name,
            "collection": self.collection_name,
            "filter": {"username": username}
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print(response.json())
        print("\033[42mDATABASE: User information fetched\033[0m")
        return response.json()['document']
    
        # Method to add new user
    async def add_user(self, item):
        print("\033[42mDATABASE: Adding new user\033[0m")
        url = f"{self.base_url}/action/insertOne"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
            "document": item
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print("\033[42mDATABASE: New user added\033[0m")
        return response.json()
    
    # Method to update a user information
    async def update_user_info(self, account_id, updated_fields):
        # for item in self.product_backlog_items:
        #     if item['_id'] == item_id:
        #         for key, value in updated_fields.items():
        #             item[key] = value
                # return item
        print("\033[42mDATABASE: Updating user info\033[0m", str(updated_fields))
        url = f"{self.base_url}/action/updateOne"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
            "filter": {"_id": {"$oid": account_id}},
            "update": {"$set": updated_fields}
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print(response.json())
        return response.json()
    
if __name__ == "__main__":
    data_api = UserData()

    async def main():
        # Get all sprints
        items = await data_api.get_all_users() 
        for item in items:
            print(json.dumps(item, indent=4))

    asyncio.run(main())