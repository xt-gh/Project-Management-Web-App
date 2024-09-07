from flet import *
from data.manage_data import Data

class DataFilter():
    def __init__(self):
        self.data = Data()
        self.selected_tag = None

    # This function sets the selected tag from the popup menu
    def set_selected_tagf(self, e, tag):
        self.selected_tag = tag

    # # This function will filter tasks based on the selected tag
    # def handle_filter_item(self, e):
    #     # If no tag is selected or "All Tasks" is chosen, show all items
    #     if self.selected_tag and self.selected_tag != "All Tasks":
    #         filtered_items = {
    #             key: item for key, item in self.data.get_product_backlog_items().items()
    #             if item['tag'] == self.selected_tag
    #         }
    #     else:
    #         # Show all items if "All Tasks" is selected
    #         filtered_items = self.data.get_product_backlog_items()
        
    #     return filtered_items

     # This function filters tasks based on the selected tag
    def handle_filter_item(self):
        product_backlog_items = self.data.get_product_backlog_items()
        filtered_items = {}

        # Filter items based on the selected tag
        for key, item in product_backlog_items.items():
            if item['tag'] == self.selected_tag:
                filtered_items[key] = item

        return filtered_items
