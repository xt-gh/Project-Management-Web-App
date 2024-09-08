from flet import *
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

        # board.controls.sort(key=lambda container: int(container.content.story_points))
        
        return Container(
            content=Column([
                        Row([
                            Text("Product Backlog", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
                            ElevatedButton("Add item", icon="add", on_click=self.handle_add_item),
                            self.filter_pop_up_button(),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Container(
                            content=self.board,
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

        # Update the page after modifying the board controls
        self.page.update()

        
