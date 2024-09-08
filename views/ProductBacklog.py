from flet import *
import flet as ft
from .components.ItemCard import ItemCard
from .components.ItemForm import ItemForm
from data.manage_data import Data

class ProductBacklog(Column):
    def __init__(self, page, update_active_view):
        super().__init__()
        self.data = Data()
        self.page = page
        self.update_active_view = update_active_view
        print(page.height)
        self.sort_options = ["High to Low", "Low to High", "Oldest to Newest"]

        
        # Initialize the MenuBar for sorting menu
        self.sort_dropdown = Dropdown(
            label="Sort by",
            hint_text="Select sorting option",
            options=[dropdown.Option(option) for option in self.sort_options]
        )

        self.sort_menu_button = PopupMenuButton(
            icon="sort",
            icon_color="black",
            items=[
                PopupMenuItem(text="High to Low", on_click=lambda e: self.handle_sort_option("High to Low")),
                PopupMenuItem(text="Low to High", on_click=lambda e: self.handle_sort_option("Low to High")),
                PopupMenuItem(text="Oldest to Newest", on_click=lambda e: self.handle_sort_option("Oldest to Newest")),
                PopupMenuItem(text="Newest to Oldest", on_click=lambda e: self.handle_sort_option("Newest to Oldest")),
            ]
        )


    def build(self):

        board = GridView(
            expand=1,
            # runs_count=3,
            max_extent=300,
            child_aspect_ratio=1.5,
            # horizontal=True,
            spacing=10,
            run_spacing=10,
            padding=padding.all(5),
        )

        product_backlog_items = self.data.get_product_backlog_items()

        for key in product_backlog_items.keys():
            board.controls.append(
                Container(
                    content=ItemCard(item_id=key, handle_detailed_view=self.handle_detailed_view),
                    alignment=alignment.center,
                )
            )
        
        return Container(
            content=Column([
                        Row([
                            Text("Product Backlog", color=colors.GREEN_800, size=24),
                            ElevatedButton("Add item", icon="add", on_click=self.handle_add_item),
                            self.sort_menu_button,
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Container(
                            content=board,
                            # bgcolor="pink",
                        )
                    ]),
            bgcolor="#CADEED",
            width=self.page.width - 300,
            height=self.page.height - 30,
            padding=padding.all(15),
            border_radius=border_radius.all(10),
        )

    def handle_add_item(self, e):
        print("Add item clicked")

        self.item_form = ItemForm(self.page, self.close_add_item_form)
        
        self.page.open(self.item_form)
    
    def handle_detailed_view(self, id):
        print("Detailed view clicked")

        self.detailed_view = ItemForm(self.page, self.close_detailed_view, mode="view", id=id)
        self.page.open(self.detailed_view)

    def close_add_item_form(self):
        print("Closing form")
        print(self.data.get_product_backlog_items())
        self.page.close(self.item_form)
        self.update_active_view()

    def close_detailed_view(self):
        print("Closing detailed view")
        self.page.close(self.detailed_view)
        self.update_active_view()
    

    def handle_sort_option(self, e):
        selected_option = e # Get the selected value from the dropdown
        if selected_option == "High to Low":
            self.sort_high_to_low()
        elif selected_option == "Low to High":
            self.sort_low_to_high()
        elif selected_option == "Oldest to Newest":
            self.sort_oldest_to_newest()
        elif selected_option == "Newest to Oldest":
            self.sort_newest_to_oldest()
        self.page.update()
    
    def sort_low_to_high(self):
        self.board.controls.sort(key=lambda container: self.priority_value(container.content.priority), reverse=False)
        self.page.update()

    def sort_high_to_low(self):
        self.board.controls.sort(key=lambda container: self.priority_value(container.content.priority), reverse=True)
        self.page.update()

    def sort_oldest_to_newest(self):
        product_backlog_items = self.data.get_product_backlog_items()

        self.board.controls.clear()
        for key in product_backlog_items.keys():
            self.board.controls.append(
                Container(
                    content=ItemCard(item_id=key, handle_detailed_view=self.handle_detailed_view),
                    alignment=alignment.center,
                )
            )
        
        self.board.controls.reverse() # This works because items are retrived in chronological order
        # Will need to add a creation_date attribute to the data base soon

    def sort_newest_to_oldest(self):
        product_backlog_items = self.data.get_product_backlog_items()

        self.board.controls.clear()
        for key in product_backlog_items.key():
            self.board.controls.append(
                Container(
                    content=ItemCard(item_id=key, handle_detailed_view=self.handle_detailed_view),
                    alignment=alignment.center,
                )
            )


    def priority_value(self, priority):
        priorities = ["Low", "Medium", "Important", "Urgent"]
        priority_level = priorities.index(priority) + 1
        return priority_level