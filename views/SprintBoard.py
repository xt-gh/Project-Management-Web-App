from flet import *
# from .components.SprintForm import SprintForm
from .components.SortPopupButton import SortPopupButton
from .components.FilterPopupButton import FilterPopupButton
import asyncio



class SprintBoard(Container):
    def __init__(self, page, data="This is the Sprint Board"):
        print("Sprint board initialized")
        super().__init__()
        self.data = data
        self.page = page

        self.bgcolor = "#CADEED"
        self.padding = padding.all(15)
        self.border_radius = border_radius.all(10)

        self.content = Text(self.data, color="black", size=32)

    def handle_click(self, e):
        # Logic that runs when the SprintBoard is clicked
        print("SprintBoard clicked!")
        self.page.snack_bar = SnackBar(Text("Sprint Board Clicked!"), open=True)
        self.page.update()

    def build(self):
        print("Building product backlog")

        self.board = GridView(
            expand=1,
            max_extent=300,
            child_aspect_ratio=1.40,
            spacing=10,
            run_spacing=10,
            padding=padding.all(5),
        )

        self.loading_screen = Container(
            content=Column([
                    ProgressRing(width=30, height=30, stroke_width=5),
                    Text("Retriving from database...", color=colors.BLACK, size=20)
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER),
            expand=1,
        )
    
        self.body = self.loading_screen

        return Container(
            content=Column([
                        Row([
                            Text("Product Backlog", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
                            Row([
                                SortPopupButton(self.handle_sort_option),
                                FilterPopupButton(self.filter_selected_tag),
                                ElevatedButton("Add item", icon="add", on_click=self.handle_add_item),
                            ], alignment=MainAxisAlignment.END),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        Container(
                            content=self.body,
                            alignment=alignment.center,
                            expand=1,
                        )
                    ]),
            padding=padding.all(20),
            border_radius=border_radius.all(10),
            bgcolor="#CADEED",
            width=self.page.width - 330,
            height=self.page.height - 20,
        )
    
    def before_update(self):
        print("\033[33mSprint board updated\033[0m")
        try: 
            if self.page:
                self.width = self.page.width - 330
                self.height =  self.page.height - 20
        except Exception as e:
            print(e)


