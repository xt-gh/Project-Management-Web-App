from flet import *

class SortPopupButton(PopupMenuButton):
    def __init__(self, handle_sort_option):
        super().__init__()
        self.icon = "sort"
        self.icon_color = "black"
        self.items = [
            PopupMenuItem(text="High to Low Priority", on_click=lambda e: handle_sort_option("High to Low Priority")),
            PopupMenuItem(text="Low to High Priority", on_click=lambda e: handle_sort_option("Low to High Priority")),
            PopupMenuItem(text="Oldest to Newest", on_click=lambda e: handle_sort_option("Oldest to Newest")),
            PopupMenuItem(text="Newest to Oldest", on_click=lambda e: handle_sort_option("Newest to Oldest")),
        ]
        self.tooltip="Sort"