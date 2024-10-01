import requests
import json

class ColourData():
    base_url = 'https://ap-southeast-1.aws.data.mongodb-api.com/app/data-vevzgeu/endpoint/data/v1'
    api_key = 'oFUhaqY07FnEp8S3hU4Bw8bxTMHM4plR3kWxT1856Wt3Hc0iiUjcn3vrhzDzLoyK'  
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }
    database_name = "projectDatabase"
    collection_name = "colour"

    # Method to get all color items
    async def get_color_items(self):
        print("\033[42mDATABASE: Getting color items\033[0m")
        url = f"{self.base_url}/action/find"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print("\033[42mDATABASE: Color items fetched\033[0m")
        for item in response.json()['documents']:
            print(item)
        return response.json()['documents']

    async def save_background_color(self, component, color):
        print(f"SAVING: Background color for {component} - {color}")
        url = f"{self.base_url}/action/updateOne"
        payload = json.dumps({
            "dataSource": "helium",
            "database": self.database_name,
            "collection": self.collection_name,
            "filter": {"component": component},  # Ensure you have a unique component
            "update": {"$set": {"background_color": color}}
        })
        response = requests.post(url, headers=self.headers, data=payload)
        print("DATABASE: Background color updated:", response.json())