from flet import *

class SideBar(Column):
    def __init__(self, data, page):
        super().__init__()
        self.data = data
        self.page = page
        self.navigator = Container(
                            content=Column(
                                controls=[
                                    Text("View", color="white", size=35),
                                    ElevatedButton("Product Backlog", bgcolor="#DAE9FE", color="374375", on_click=lambda e: self.page.go("/productbacklog")),
                                    ElevatedButton("Sprintboard", bgcolor="#DAE9FE", color="374375", on_click=lambda e: self.page.go("/sprintboard")),
                                    ElevatedButton("Collaborators", bgcolor="#DAE9FE", color="374375", on_click=lambda e: self.page.go("/sprint")),
                                ],
                            ),
                            bgcolor="#6686BD",
                            padding=10,
                            border_radius=border_radius.all(10),
                            width=300,
                            height=self.page.height - 144,
                            # expand=True,
                        )


    def build(self):
        return (
            Container(
                content=Column([
                    Text("Project Title", color="black", size=45),
                    Text("Project Description/Details", color="black", size=16),
                    self.navigator,
                ], alignment=MainAxisAlignment.START),
                padding=padding.all(15),
                margin=margin.all(0),
                width=300,
            )
        )
    
    