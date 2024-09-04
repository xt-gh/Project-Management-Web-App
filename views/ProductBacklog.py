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
        print(page.height)

    def build(self):

        board = GridView(
            expand=1,
            runs_count=3,
            max_extent=300,
            child_aspect_ratio=3,
            spacing=10,
            run_spacing=10,
            padding=padding.all(5),
            width=1000,
            height=self.page.height * 0.7,
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
                            IconButton(
                                icon=icons.ADD,
                                icon_color="black",
                                on_click=self.handle_add_item
                            )
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Container(
                            content=board,
                            bgcolor="pink",
                        )
                    ]),
            bgcolor="#CADEED",
            width=self.page.width * 0.7,
            height=self.page.height * 0.9,
            padding=padding.all(15),
            border_radius=border_radius.all(10),
        )

    def handle_add_item(self, e):
        print("Add item clicked")

        self.item_form = AlertDialog(
            content=ItemForm(self.page, self.close_form),
            on_dismiss=lambda e: print("Item form dismissed!"),
            bgcolor="#CADEED",
            clip_behavior=ClipBehavior.HARD_EDGE
        )
        
        self.page.open(self.item_form)

    def add_item(self, item):
        print(vars(item))
    
    def handle_detailed_view(self, e):
        print("Detailed view clicked")

    def close_form(self):
        print("Closing form")
        print(self.data.get_product_backlog_items())
        self.page.close(self.item_form)
        self.update_active_view()