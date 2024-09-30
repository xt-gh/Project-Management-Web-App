from flet import *

class SprintKanbanView(Column):
    def __init__(self, page):
        super().__init__()
        print("Sprint kanban initialized")
        self.page = page

        self.bgcolor = "#CADEED"
        self.padding = padding.all(15)
        self.border_radius = border_radius.all(10)
        

    def build(self):
        print("Building Sprint kanban board")

        self.not_started_column = Container(
            content=Column([
                Row([Text("Not Started", weight=FontWeight.W_500, color=colors.BLACK, size=30)], alignment=MainAxisAlignment.CENTER),
                Column([
                    Text("Not Started", color=colors.BLACK, size=20),
                    Text("Not Started", color=colors.BLACK, size=20),
                    Text("Not Started", color=colors.BLACK, size=20),
                ])
            ]),
            bgcolor="#E7A4A4",
            border=border.all(1.5, "#000000"),
            border_radius=border_radius.all(10),
            padding=padding.all(10),
            expand=True,
            height=self.page.height - 120,
        )

        self.in_progress_column = Container(
            content=Column([
                Row([Text("In Progress", weight=FontWeight.W_500, color=colors.BLACK, size=30)], alignment=MainAxisAlignment.CENTER),
                Column([
                    Text("In Progress", color=colors.BLACK, size=20),
                    Text("In Progress", color=colors.BLACK, size=20),
                    Text("In Progress", color=colors.BLACK, size=20),
                ])
            ]),
            bgcolor="#E6DEB3",
            border=border.all(1.5, "#000000"),
            border_radius=border_radius.all(10),
            padding=padding.all(10),
            expand=True,
            height=self.page.height - 120,
        )

        self.completed_column = Container(
            content=Column([
                Row([Text("Completed", weight=FontWeight.W_500, color=colors.BLACK, size=30)], alignment=MainAxisAlignment.CENTER),
                Column([
                    Text("Completed", color=colors.BLACK, size=20),
                    Text("Completed", color=colors.BLACK, size=20),
                    Text("Completed", color=colors.BLACK, size=20),
                ])
            ]),
            bgcolor="#AED0AE",
            border=border.all(1.5, "#000000"),
            border_radius=border_radius.all(10),
            padding=padding.all(10),
            expand=True,
            height=self.page.height - 120,
        )


        return Container(
            content=Column([
                Row([
                    Text("Sprint Kanban", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
                    Row([
                        ElevatedButton("Burndown Chart", icon=icons.SSID_CHART, on_click=lambda e: print("Burndown chart clicked")),
                        IconButton(icon=icons.CLOSE, on_click=lambda e: print("Close sprint kanban")),
                    ])
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Container(
                    content=Row([
                        self.not_started_column,
                        self.in_progress_column,
                        self.completed_column,
                    ])
                )
            ]),
            padding=padding.all(20),
            border_radius=border_radius.all(10),
            bgcolor="#CADEED",
            width=self.page.width - 330,
            height=self.page.height - 20,
        )
    
    
    def before_update(self):
        print("\033[33mSprint kanban board updated\033[0m")
        if self.page:
            self.controls[0].width = self.page.width - 330
            self.controls[0].height =  self.page.height - 20

            self.controls[0].content.controls[1].content.controls[0].height = self.page.height - 120
            self.controls[0].content.controls[1].content.controls[1].height = self.page.height - 120
            self.controls[0].content.controls[1].content.controls[2].height = self.page.height - 120