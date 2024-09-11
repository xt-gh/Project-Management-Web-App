from flet import *

class FilterPopupButton(PopupMenuButton):
    def __init__(self, filter_selected_tag):
        super().__init__()
        self.icon = "filter_alt"
        self.icon_color = "black"
        self.items = [
            PopupMenuItem(text="All Tasks", on_click=lambda _: filter_selected_tag("All Tasks")),
            PopupMenuItem(text="API", on_click=lambda _: filter_selected_tag("API")),
            PopupMenuItem(text="Back-end", on_click=lambda _: filter_selected_tag("Back-end")),
            PopupMenuItem(text="Database", on_click=lambda _: filter_selected_tag("Database")),
            PopupMenuItem(text="Framework", on_click=lambda _: filter_selected_tag("Framework")),
            PopupMenuItem(text="Front-end", on_click=lambda _: filter_selected_tag("Front-end")),
            PopupMenuItem(text="Testing", on_click=lambda _: filter_selected_tag("Testing")),
            PopupMenuItem(text="UI", on_click=lambda _: filter_selected_tag("UI")),
            PopupMenuItem(text="UX", on_click=lambda _: filter_selected_tag("UX"))   
        ]