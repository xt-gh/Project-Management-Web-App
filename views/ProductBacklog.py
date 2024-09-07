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
        self.show_filter_options = False  # Toggle visibility of filter options

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

        # ElevatedButton to show or hide filter options
        self.filter_button = ElevatedButton(
            text="Filter Tasks",
            icon="filter_alt",
            on_click=self.toggle_filter_options  # Toggle the list of options when clicked
        )

        # Column to hold filter options (Initially hidden)
        self.filter_options = Column(
            visible=self.show_filter_options,  # Controlled by self.show_filter_options
            controls=[
                TextButton("Front-end", on_click=lambda e: self.apply_filter("Front-end")),
                TextButton("Back-end", on_click=lambda e: self.apply_filter("Back-end")),
                TextButton("API", on_click=lambda e: self.apply_filter("API")),
                TextButton("Database", on_click=lambda e: self.apply_filter("Database")),
                TextButton("UI", on_click=lambda e: self.apply_filter("UI")),
                TextButton("UX", on_click=lambda e: self.apply_filter("UX")),
                TextButton("Testing", on_click=lambda e: self.apply_filter("Testing")),
                TextButton("Framework", on_click=lambda e: self.apply_filter("Framework")),
                TextButton("All Tasks", on_click=lambda e: self.apply_filter("All Tasks")),
            ]
        )

        return Container(
            content=Column([
                        Row([
                            Text("Product Backlog", color=colors.GREEN_800, size=24),
                            ElevatedButton("Add item", icon="add", on_click=self.handle_add_item),
                            self.filter_button  # Filter button to show/hide options
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        self.filter_options,  # The list of options will be shown/hidden
                        Container(content=board)
                    ]),
            bgcolor="#CADEED",
            width=self.page.width - 300,
            height=self.page.height - 30,
            padding=padding.all(15),
            border_radius=border_radius.all(10),
        )

    # This function toggles the visibility of the filter options
    def toggle_filter_options(self, e):
        self.show_filter_options = not self.show_filter_options  # Toggle visibility
        self.filter_options.visible = self.show_filter_options  # Update column visibility
        self.page.update()

    # This function applies the selected filter
    def apply_filter(self, tag):
        self.selected_tag = tag
        self.handle_filter_item(None)  # Call filter logic
        self.toggle_filter_options(None)  # Hide filter options after selecting

    # This function filters tasks based on the selected tag
    def handle_filter_item(self, e):
        if self.selected_tag and self.selected_tag != "All Tasks":
            filtered_items = {
                key: item for key, item in self.data.get_product_backlog_items().items()
                if item['tag'] == self.selected_tag
            }
        else:
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