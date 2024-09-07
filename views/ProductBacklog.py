from flet import *
from .components.ItemCard import ItemCard
from .components.ItemForm import ItemForm
from data.manage_data import Data

class ProductBacklog(Column):
    def __init__(self, page, update_active_view):
        super().__init__()
        self.data = Data()
        self.page = page
        self.update_active_view = update_active_view
        self.selected_tag = None # to store the selected tag
        print(page.height)

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

        self.filter_pop_up_button()
        # board.controls.sort(key=lambda container: int(container.content.story_points))
        
        return Container(
            content=Column([
                        Row([
                            Text("Product Backlog", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
                            ElevatedButton("Add item", icon="add", on_click=self.handle_add_item),
                            self.filter_menu_button,
                            self.filter_button,
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
    
    def set_selected_tag(self,e,tag):
        self.selected_tag = tag

    def filter_pop_up_button(self):
        # Create PopupMenuButton for task filtering
        self.filter_menu_button = PopupMenuButton(
            icon="filter_alt",

            items=[
                PopupMenuItem(text="Front-end", on_click=lambda e: self.set_selected_tag(e, "Front-end")),
                PopupMenuItem(text="Back-end", on_click=lambda e: self.set_selected_tag(e, "Back-end")),
                PopupMenuItem(text="API", on_click=lambda e: self.set_selected_tag(e, "API")),
                PopupMenuItem(text="Database", on_click=lambda e: self.set_selected_tag(e, "Database")),
                PopupMenuItem(text="UI", on_click=lambda e: self.set_selected_tag(e, "UI")),
                PopupMenuItem(text="UX", on_click=lambda e: self.set_selected_tag(e, "UX")),
                PopupMenuItem(text="Testing", on_click=lambda e: self.set_selected_tag(e, "Testing")),
                PopupMenuItem(text="Framework", on_click=lambda e: self.set_selected_tag(e, "Framework")),
                PopupMenuItem(text="All Tasks", on_click=lambda e: self.set_selected_tag(e, "All Tasks"))
            ]
        )

        # Create ElevatedButton to apply the filter
        self.filter_button = ElevatedButton(
            text="Apply Filter",
            icon="filter_alt",
            on_click=self.handle_filter_item  # Apply filter when clicked
        )

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

    