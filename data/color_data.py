from bson.objectid import ObjectId
from data.db import db

class ColourData():
    collection_name = "colour"
    collection = db[collection_name]

    # Method to get all color items
    async def get_color_items(self):
        print("\033[42mDATABASE: Getting color items\033[0m")
        documents = list(self.collection.find({}))
        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        print("\033[42mDATABASE: Color items fetched\033[0m")
        for item in documents:
            print(item)
        return documents

    async def save_background_color(self, component, color):
        print(f"SAVING: Background color for {component} - {color}")
        result = self.collection.update_one(
            {"component": component},
            {"$set": {"background_color": color}},
            upsert=True
        )
        print("DATABASE: Background color updated")
        return {
            "matchedCount": result.matched_count,
            "modifiedCount": result.modified_count,
            "upsertedId": str(result.upserted_id) if result.upserted_id else None
        }