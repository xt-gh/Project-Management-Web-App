2101
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
        self.selected_tag = None  # To store the selected tag

    def build(self):

        board = GridView(
            expand=1,
            max_extent=300,
            child_aspect_ratio=1.5,
            spacing=10,
            run_spacing=10,
            padding=padding.all(5),
        )

        product_backlog_items = self.data.get_product_backlog_items()

        # Add the items to the board
        for key in product_backlog_items.keys():
            board.controls.append(
                Container(
                    content=ItemCard(item_id=key, handle_detailed_view=self.handle_detailed_view),
                    alignment=alignment.center,
                )
            )

        # Create Dropdown for task filtering
        self.filter_dropdown = Dropdown(
            label="Task Tags",
            hint_text="Choose a task tag",
            options=[
                dropdown.Option("Front-end"),
                dropdown.Option("Back-end"),
                dropdown.Option("API"),
                dropdown.Option("Database"),
                dropdown.Option("UI"),
                dropdown.Option("UX"),
                dropdown.Option("Testing"),
                dropdown.Option("Framework"),
                dropdown.Option("All Tasks"),  # Option to show all tasks
            ],
            on_change=self.set_selected_tag  # Capture the selected tag
        )

        # Create ElevatedButton to apply the filter
        self.filter_button = ElevatedButton(
            text="Apply Filter",
            icon="filter_alt",
            on_click=self.handle_filter_item  # Apply filter when clicked
        )

        return Container(
            content=Column([
                        Row([
                            Text("Product Backlog", color=colors.GREEN_800, size=24),
                            ElevatedButton("Add item", icon="add", on_click=self.handle_add_item),
                            self.filter_dropdown,
                            self.filter_button
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        Container(content=board)
                    ]),
            bgcolor="#CADEED",
            width=self.page.width - 300,
            height=self.page.height - 30,
            padding=padding.all(15),
            border_radius=border_radius.all(10),
        )

    # This function sets the selected tag from the dropdown
    def set_selected_tag(self, e):
        self.selected_tag = e.control.value

    # This function will filter tasks based on the selected tag
    def handle_filter_item(self, e):
        # If no tag is selected or "All Tasks" is chosen, show all items
        if self.selected_tag and self.selected_tag != "All Tasks":
            filtered_items = {
                key: item for key, item in self.data.get_product_backlog_items().items()
                if item['tag'] == self.selected_tag
            }
        else:
            # Show all items if "All Tasks" is selected
            filtered_items = self.data.get_product_backlog_items()

        # Update the UI with the filtered tasks
        self.update_board(filtered_items)

    # This function updates the board with the filtered items
    def update_board(self, filtered_items):
        board = GridView(
            expand=1,
            max_extent=300,
            child_aspect_ratio=1.5,
            spacing=10,
            run_spacing=10,
            padding=padding.all(5),
        )

        # Add the filtered items to the board
        for key in filtered_items.keys():
            board.controls.append(
                Container(
                    content=ItemCard(item_id=key, handle_detailed_view=self.handle_detailed_view),
                    alignment=alignment.center,
                )
            )

        # Replace the old board with the new filtered board
        self.page.controls[-1] = board
        self.page.update()

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
        self.page.close(self.item_form)
        self.update_active_view()

    def close_detailed_view(self):
        print("Closing detailed view")
        self.page.close(self.detailed_view)
        self.update_active_view()
