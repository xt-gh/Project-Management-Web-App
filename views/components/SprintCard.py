from flet import *
from data.manage_data import Data
import asyncio
from datetime import datetime

class SprintCard(Container):
    def __init__(self, page, sprint_dict, handle_detailed_view=None):
        print("Sprint card initialized")
        super().__init__()

        self.page = page
        self.id = sprint_dict["_id"]
        self.sprint_name = sprint_dict["sprint_name"]
        self.product_owner = sprint_dict["product_owner"]  
        self.scrum_master = sprint_dict["scrum_master"]
        self.scrum_team = sprint_dict["scrum_team"]
        self.start_date = sprint_dict["start_date"]
        self.end_date = sprint_dict["end_date"]

        self.status = "Placeholder"


        self.handle_detailed_view = handle_detailed_view

        self.bgcolor = "#BABDE2"
        self.border = border.all(1.5, "#000000")
        self.border_radius = border_radius.all(10)
        self.padding = padding.all(10)
        self.margin = margin.all(8)
        self.expand = 1
        self.ink = True
        self.on_click = lambda e: self.handle_on_click()
        self.content = Column([
            self.card_title(),
            self.card_details()
        ])

    def handle_on_click(self):
        print("Clickable without Ink clicked!")
        # self.page.go("/sprintkanban/" + self.id)


    def card_title(self):
        return Container(
            content=Text(
                self.sprint_name,
                color="black", 
                size=20,
                max_lines=2,
                expand=1,
                overflow=TextOverflow.ELLIPSIS
            )
        )

    def card_details(self):
        details = Row([
            Column(),
            # But buttons below are temporary, only for development purposes
            ElevatedButton(
                "DEV: click to see sprint details", 
                icon=icons.MONITOR, 
                on_click=lambda e: (print("Sprint details clicked"), self.page.go("/sprintbacklog/" + self.id))
            ),
            ElevatedButton(
                "DEV: click to see sprint kanban", 
                icon=icons.MONITOR, 
                on_click=lambda e: (print("Sprint kanban clicked"), self.page.go("/sprintkanban/" + self.id))
            ),
            IconButton(
                icon=icons.MORE_HORIZ_ROUNDED,
                icon_color="black",
                icon_size=20,
                on_click=lambda e: self.handle_detailed_view(self.id),
                hover_color="#F1F1F1",

            )
        ], 
        alignment=MainAxisAlignment.END,
        # tight=True,
        )

        if self.start_date:
            details.controls[0].controls.insert(
                0,
                Container(Text(f"Start Date: {self.start_date} ", color="black", size=14)),
            )
            details.alignment=MainAxisAlignment.SPACE_BETWEEN

        if self.end_date:
            details.controls[0].controls.insert(
                0,
                Container(Text(f"End Date: {self.end_date} ", color="black", size=14)),
            )
            details.alignment=MainAxisAlignment.SPACE_BETWEEN

        if self.status:
            details.controls[0].controls.insert(
                0,
                Container(Text(f"Status: {self.status} ", color="black", size=14)),
            )
            details.alignment=MainAxisAlignment.SPACE_BETWEEN

        return details