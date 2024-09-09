from flet import *
import flet as ft
from .components.ItemCard import ItemCard
from .components.ItemForm import ItemForm
from data.manage_data import Data
from data.filter_data import DataFilter 

class ProductBacklog(Column):
    def __init__(self, page, update_active_view):
        super().__init__()
        self.data = Data()
        self.page = page
        self.update_active_view = update_active_view
        self.filter_data = DataFilter()

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

        self.board = GridView(
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
            self.board.controls.append(
                Container(
                    content=ItemCard(item_id=key, handle_detailed_view=self.handle_detailed_view),
                    alignment=alignment.center,
                )
            )
        
        return Container(
            content=Column([
                        Row([
                            Text("Product Backlog", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
                            ElevatedButton("Add item", icon="add", on_click=self.handle_add_item),
                            self.sort_menu_button,
                            self.filter_pop_up_button(),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Container(
                            content=self.board,
                            # bgcolor="pink",
                        )
                    ]),
            bgcolor="#CADEED",
            width=1115,
            height=self.page.height - 20,
            padding=padding.all(20),
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
    
    def filter_pop_up_button(self):
        # Create PopupMenuButton for task filtering
        self.filter_menu_button = PopupMenuButton(
            icon="filter_alt", icon_color='black',
            items=[
                PopupMenuItem(text="All Tasks", on_click=lambda _: self.filter_selected_tag("All Tasks")),
                PopupMenuItem(text="API", on_click=lambda _: self.filter_selected_tag("API")),
                PopupMenuItem(text="Back-end", on_click=lambda _: self.filter_selected_tag("Back-end")),
                PopupMenuItem(text="Database", on_click=lambda _: self.filter_selected_tag("Database")),
                PopupMenuItem(text="Framework", on_click=lambda _: self.filter_selected_tag("Framework")),
                PopupMenuItem(text="Front-end", on_click=lambda _: self.filter_selected_tag("Front-end")),
                PopupMenuItem(text="Testing", on_click=lambda _: self.filter_selected_tag("Testing")),
                PopupMenuItem(text="UI", on_click=lambda _: self.filter_selected_tag("UI")),
                PopupMenuItem(text="UX", on_click=lambda _: self.filter_selected_tag("UX"))   
            ]
        )
        return self.filter_menu_button
    
    def filter_selected_tag(self, tag):
        print(f"Tag selected: {tag}")
        self.filter_data.set_selected_filtered_tag(tag)
        self.apply_filter()

    def apply_filter(self):
        filtered_items = self.filter_data.handle_filter_item()
        self.update_board(filtered_items)

    def update_board(self, filtered_items):
        # Clear the existing board content
        self.board.controls.clear()

        for key in filtered_items.keys():
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

        # Update the page after modifying the board controls
        self.page.update()

        
