from flet import *
from data.color_data import ColourData
import asyncio

class SideBar(Column):
    def __init__(self, page):
        print("Sidebar initialized")
        super().__init__()
        self.page = page
        self.navigator = Container(
                            content=Column(
                                controls=[
                                    Text("View", color="white", size=35),
                                    ElevatedButton(
                                        content=Container(
                                            Text("Product Backlog", color="black", size=20),
                                            width=250,
                                            padding=padding.only(0, 3, 0, 0)
                                        ),
                                        bgcolor="#DAE9FE",
                                        color="374375",
                                        on_click=lambda e: self.page.go("/productbacklog")
                                    ),
                                    ElevatedButton(
                                        content=Container(
                                            Text("Sprint Board", color="black", size=20), 
                                            width=250,
                                            padding=padding.only(0, 3, 0, 0)
                                        ),
                                        bgcolor="#DAE9FE",
                                        color="374375",
                                        on_click=lambda e: self.page.go("/sprintboard")
                                    ),
                                    ElevatedButton(
                                        content=Container(
                                            Text("Collaborators", color="black", size=20),
                                            width=250,
                                            padding=padding.only(0, 3, 0, 0)
                                        ),
                                        bgcolor="#DAE9FE",
                                        color="374375",
                                        on_click=lambda e: self.page.go("/collaborators")
                                    ),
                                ],
                            ),
                            bgcolor="#6686BD",
                            padding=10,
                            border_radius=border_radius.all(10),
                            width=300,
                            height=self.page.height - 230,
                            expand=True,
                        )
    
    
    def build(self):
        print("Building sidebar")
        return (
            Container(
                content=Column([
                    Container(Text("Agile Master", color="black", size=54), padding=padding.only(0, 20, 0, 0)),
                    self.navigator,
                ], alignment=MainAxisAlignment.START),
                padding=padding.all(15),
                margin=margin.all(0),
                border_radius=10,
                height=900,
                width=300,
            )
        )

    def before_update(self):
        print("Sidebar updated")
        if self.page:
            self.navigator.height = self.page.height - 230

    async def load_initial_background_color(self):
        color_item = await ColourData().get_color_items()  # Get color items
        for item in color_item:
            if item['component'] == "Side Bar":
                self.bg_color = item['background_color']
                self.controls[0].bgcolor = self.bg_color
            elif item['component'] == "Side Bar Navigator":
                self.navigator.bgcolor = item['background_color']
                self.bgcolor = self.navigator.bgcolor     

    def did_mount(self):
        print("\033[33mSidebar mounted\033[0m")
        asyncio.run(self.load_initial_background_color())

    def change_bg_colour(self, selected_color):
        """Change the background color of the product backlog."""
        self.bg_color = selected_color
        self.controls[0].bgcolor = self.bg_color  # Update the container's background
        self.page.update()
        asyncio.run(ColourData().save_background_color("Side Bar", self.bg_color))

    def change_navigator_bg_colour(self, selected_color):
        """Change the background color of the product backlog."""
        self.navigator.bgcolor = selected_color
        self.bgcolor = self.navigator.bgcolor  # Update the container's background
        self.page.update()
        asyncio.run(ColourData().save_background_color("Side Bar Navigator", self.navigator.bgcolor))