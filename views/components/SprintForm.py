from flet import *
from .FormComponents import DropdownInput, TextFieldInput, MultipleSelectInput
from data.manage_data import Data
from datetime import datetime
import asyncio


class SprintFrom(AlertDialog):
    def __init__(self, page, close_form, mode="add", item_dict=None):
        print("Item form initialized")
        super().__init__
        self.page = page
        self.close_form = close_form
        self.mode = mode # Mode can be "add" or "view" or "edit"
        self.item_dict = item_dict # type: ignore
        # self.data = Data()
        self.content_padding = 10

        self.inset_padding = 10

        self.status_options = ["Not Started", "In progress", "Completed"]
        self.bgcolor = "#CADEED"
        self.clip_behavior = ClipBehavior.HARD_EDGE

        self.content = self.build_add_sprint_form()
        self.inset_padding = 10
        self.actions_padding = 20

    
    def build_add_sprint_form(self):
        self.sprint_name = TextFieldInput(label="Sprint Name", is_required=True)
        self.start_date = DatePicker(first_date=datetime.datetime(year=2023, month=10, day=1),
                    last_date=datetime.datetime(year=2024, month=10, day=1),
                )
        self.end_date = DatePicker(first_date=datetime.datetime(year=2023, month=10, day=1),
                    last_date=datetime.datetime(year=2024, month=10, day=1),
                )
        
        self.status = Dropdown(label="Status", options=[dropdown.Option(x) for x in self.status_options])

        self.tag_container = Row(wrap=True)
        self.assignee_input = TextField(label="Assigne to: ", width=200)
        self.add_assignee_button = ElevatedButton("Add Assignee", on_click=self.add_assignee)
        self.assignee_tags = MultipleSelectInput(self.assignee)
        self.task_logs = Row([Text(" ", color="black", size = 15),])

        self.footer = [
            ElevatedButton("Cancel", bgcolor=colors.RED_300, width=100, color="black", on_click=lambda e: self.close_form()),
            ElevatedButton("Save", bgcolor=colors.GREEN_300, width=100, color="black", on_click=lambda e: self.handle_submit()),
        ]

        self.actions = self.footer

        self.header =[Text("Add Item" if self.mode == "add" else "Editiing Iten", color="black", size=24)]

        if self.mode != "add" and self.item_dict:
            self.sprint_name.value = self.item_dict.get("sprint_name", "")
            self.start_date.value = self.item_dict.get("start_date", "")
            self.end_date.value = self.item_dict.get("end_date", "")
            self.status.value = self.item_dict.get("status", "")
            self.assignees = self.item_dict.get("assignee_tags", [])
            self.update_tags()

        # if self.mode == "add":
        #     self.header = [Text("Add Item", color="black", size=24)]

        # else:
        #     self.header = [
        #         Text("Editing Item", color="black", size=24),
        #         IconButton(
        #             icon=icons.DELETE_FOREVER,
        #             icon_color="black",
        #             on_click=lambda e: (asyncio.run(Data().remove_product_backlog_item(self.item_dict["_id"])), self.close_form()),
        #         )
        #     ]

         # Combine all components into the form layout
            form_content = Column(
                [
                    self.sprint_name,
                    self.start_date,
                    self.end_date,
                    self.status,
                    Row([self.assignee_input, self.add_button]),
                    Text("Assignees:"),
                    self.tag_container,
                ],
                spacing=10
            )
            
            return form_content
        
    def add_assignee(self, e):
        assignee_name = slef.assignee_input.value.strip()
        if assignee_name:
            assignees.append(assignee_name)
            self.assignee_input.value = ""  # Clear input field after adding
            self.update_tags()  # Refresh the tag list
        self.page.update()

    # Function to remove an assignee tag
    def remove_assignee(self, tag):
        assignees.remove(tag)  # Remove the assignee from the list
        self.update_tags()  # Refresh the tag list
        self.page.update()

    # Function to update the display of assignee tags
    def update_tags(self):
        self.tag_container.controls.clear()  # Clear current tags
        for assignee in assignees:
            # Each tag is a Row with a label and a delete button
            self.tag_container.controls.append(
                Container(
                    content=Row(
                        [
                            Text(assignee),
                            IconButton(
                                icon=icons.CLOSE,
                                on_click=lambda e, a=assignee: self.remove_assignee(a),  # Remove tag on click
                            ),
                        ],
                        spacing=5,
                    ),
                    padding=5,
                    border_radius=border_radius.all(8),
                    bgcolor=colors.LIGHT_BLUE_50,  # Color the tag background
                )
            )
        self.page.update()

    def handle_submit(self):
        # Save logic for the sprint form
        print("Form submitted.")
        # Here you would implement the actual saving logic (e.g., to a database)
        self.close_form()




            # self.sprint_name.value = item["sprint_name"]
            # self.start_date.value = item["start_date"]
            # self.end_date.value = item["end_date"]
            # self.status.value = item["status"]
            # self.assignee_tags.value = item["assignee_tags"]



