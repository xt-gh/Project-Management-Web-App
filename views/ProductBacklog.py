from flet import *
from .components.ItemCard import ItemCard
from .components.ItemForm import ItemForm

class ProductBacklog(Column):
    def __init__(self, data, page, update_active_view):
        super().__init__()
        self.data = data
        self.page = page
        self.update_active_view = update_active_view
        print(page.height)

        self.item_form = AlertDialog(
            content=ItemForm(self.data, self.page, self.close_form),
            on_dismiss=lambda e: print("Item form dismissed!"),
            bgcolor="#CADEED",
        )
    # def handle_change(self, e):
    #     print("Checkbox changed", self.cb.value)

    #     if self.cb.value:
    #         self.data.append(f"Item {len(self.data) + 1}")
        
    #     print("data:", self.data)
    #     self.update_active_view()

    def build(self):

        board = GridView(
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
            width=1000,
            height=self.page.height,
        )

        for i in range(10):
            board.controls.append(
                ItemCard(name=f"Task {i}")
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
                        board
                    ]),
            bgcolor="#CADEED",
            width=self.page.width * 0.7,
            height=self.page.height * 0.9,
            padding=padding.all(15),
            border_radius=border_radius.all(10),
        )

    def handle_add_item(self, e):
        print("Add item clicked")
        
        self.page.open(self.item_form)

    def add_item(self, item):
        print(vars(item))

    def close_form(self):
        print("Closing form")
        self.page.close(self.item_form)