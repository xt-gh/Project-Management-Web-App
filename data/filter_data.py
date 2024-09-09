from flet import *
from data.manage_data import Data

class DataFilter():
    def __init__(self):
        self.data = Data()
        self.selected_tag = None

    # Set the selected tag from the popup menu
    def set_selected_filtered_tag(self,tag):
        self.selected_tag = tag

     # Filter tasks based on the selected tag
    def handle_filter_item(self):
        product_backlog_items = self.data.get_product_backlog_items()
        filtered_items = {}

         # Filter items based on the selected tag
        if self.selected_tag and self.selected_tag != "All Tasks":
            for key, item in product_backlog_items.items():
                if self.selected_tag in item['tags']:
                    filtered_items[key] = item
        else:
            # If "All Tasks" is selected, show all items
            filtered_items = product_backlog_items

        return filtered_items
