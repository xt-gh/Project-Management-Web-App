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

        for i in range(len(self.data)):
            board.controls.append(
                Container(
                    content=ItemCard(task_name=self.data[i]),
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
            content=ItemForm(self.data, self.page, self.close_form),
            on_dismiss=lambda e: print("Item form dismissed!"),
            bgcolor="#CADEED",
        )
        
        self.page.open(self.item_form)

    def add_item(self, item):
        print(vars(item))

    def close_form(self):
        print("Closing form")
        print(self.data)
        self.page.close(self.item_form)
        self.update_active_view()