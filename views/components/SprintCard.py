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

        
        today_date_object = datetime.now().date()
        start_date_object = datetime.strptime(self.start_date, '%d-%m-%Y').date()
        end_date_object = datetime.strptime(self.end_date, '%d-%m-%Y').date()
        self.diff = end_date_object - start_date_object
        self.days_left = end_date_object - today_date_object

        if today_date_object < start_date_object:
            self.status = "Not Started"
        
        elif today_date_object > end_date_object:
            self.status = "Completed"

        else:
            self.status = "In Progress"

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
        return Row([
            Text(
                f"{self.sprint_name} ({self.status})",
                color="black", 
                size=30,
                weight=FontWeight.BOLD,
                max_lines=2,
                expand=1,
                overflow=TextOverflow.ELLIPSIS
            ),
            IconButton(
                icon=icons.EDIT_DOCUMENT,
                icon_color="black",
                icon_size=30,
                on_click=lambda e: self.handle_detailed_view(self.id),
                hover_color="#F1F1F1",
                # disabled=self.status != "Not Started",
                mouse_cursor=MouseCursor.CLICK if self.status == "Not Started" else MouseCursor.FORBIDDEN,
            )
        ],
        alignment=MainAxisAlignment.SPACE_BETWEEN
        )

    def card_details(self):
        return Row([
            self.status_details(),
            self.member_details(),
            self.controls_details()
        ],
        alignment=MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=CrossAxisAlignment.START)

    def status_details(self):
    
        status_column = Column([
            Text("Start Date: " + self.start_date, color="black", size=20),
            Text("End Date: " + self.end_date, color="black", size=20),
            Text("Duration: " + str(self.diff.days) + " days", color="black", size=20),
            Text("Days Left: " + str(max(self.days_left.days, 0)) + " days", color="black", size=20)
        ],
        alignment=MainAxisAlignment.START)
    
        return status_column

    def member_details(self):
        member_column = Column([
            Text("Product Owner: Not Assigned", color="black", size=20),
            Text("Scrum Master: Not Assigned", color="black", size=20),
            Text("Scrum Team: Not Assigned", color="black", size=20),
        ],
        alignment=MainAxisAlignment.START)
        if self.product_owner:
            member_column.controls[0].value = "Product Owner: " + self.product_owner
        if self.scrum_master:
            member_column.controls[1].value = "Scrum Master: " + self.scrum_master
        if self.scrum_team:
            member_column.controls[2].value = "Scrum Team: " + str(self.scrum_team)

        return member_column
    
    def controls_details(self):
        if self.status == "Not Started":
            return Column([
                ElevatedButton(
                    "Manage Sprint Backlog", 
                    icon=icons.DRIVE_FILE_MOVE_OUTLINED, 
                    on_click=lambda e: (print("Sprint details clicked"), self.page.go("/sprintbacklog/" + self.id))
                ),
                ElevatedButton(
                    "View Sprint Kanban", 
                    icon=icons.VIEW_KANBAN_OUTLINED, 
                    on_click=lambda e: (print("Sprint kanban clicked"), self.page.go("/sprintkanban/" + self.id))
                ),
                ElevatedButton(
                    "View Sprint Backlog", 
                    icon=icons.FEATURED_PLAY_LIST_OUTLINED, 
                    on_click=lambda e: (print("Sprint backlog clicked"), self.page.go("/sprintlist/" + self.id))
                ),
            ],
            alignment=MainAxisAlignment.START)
        
        if self.status == "In Progress":
            return Column([
                ElevatedButton(
                    "View Sprint Kanban", 
                    icon=icons.VIEW_KANBAN_OUTLINED, 
                    on_click=lambda e: (print("Sprint kanban clicked"), self.page.go("/sprintkanban/" + self.id))
                ),
                ElevatedButton(
                    "View Sprint Backlog", 
                    icon=icons.FEATURED_PLAY_LIST_OUTLINED, 
                    on_click=lambda e: (print("Sprint backlog clicked"), self.page.go("/sprintlist/" + self.id))
                ),
            ],
            alignment=MainAxisAlignment.START)

        if self.status == "Completed":
            return Column([
                ElevatedButton(
                    "View Sprint Report", 
                    icon=icons.MONITOR, 
                    on_click=lambda e: (print("Sprint report clicked"), self.page.go("/sprintreport/" + self.id))
                ),
            ],
            alignment=MainAxisAlignment.START)