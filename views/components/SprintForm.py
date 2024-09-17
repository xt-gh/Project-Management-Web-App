from flet import *
from .FormComponents import DropdownInput, TextFieldInput, MultipleSelectInput
from data.manage_data import Data
from datetime import datetime

class SprintForm(AlertDialog):
    def __init__(self, page, close_form, mode="add", item_dict=None):
        print("Item form initialized")
        super().__init__()
        self.page = page
        self.close_form = close_form
        self.mode = mode  # Mode can be "add" or "view" or "edit"
        self.item_dict = item_dict or {}
        self.content_padding = 10
        self.inset_padding = 10
        self.status_options = ["Not Started", "In progress", "Completed"]
        self.bgcolor = "#CADEED"
        self.clip_behavior = ClipBehavior.HARD_EDGE
        
        self.assignees = []

        # Build the form content
        self.content = self.build_add_sprint_form()
        self.inset_padding = 10
        self.actions_padding = 20

    def build_add_sprint_form(self):
        self.sprint_name = TextFieldInput(label="Sprint Name", is_required=True)
        
        # Start date button using the simple pattern
        self.start_date_button = ElevatedButton(
            "Pick Start Date",
            icon=icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                DatePicker(
                    first_date=datetime(year=2015, month=1, day=1),
                    last_date=datetime(year=2032, month=12, day=31),
                )
            )
        )

        # End date button using the simple pattern
        self.end_date_button = ElevatedButton(
            "Pick End Date",
            icon=icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                DatePicker(
                    first_date=datetime(year=2015, month=1, day=1),
                    last_date=datetime(year=2032, month=12, day=31),
                )
            )
        )

        self.status = Dropdown(
            label="Status", 
            options=[dropdown.Option(x) for x in self.status_options]
        )

        self.tag_container = Row(wrap=True)
        self.assignee_input = TextField(label="Assign to: ", width=200)
        self.add_assignee_button = ElevatedButton("Add Assignee", on_click=self.add_assignee)
        self.assignee_tags = MultipleSelectInput(self.assignees)
        self.task_logs = Row([Text(" ", color="black", size=15),])

        self.footer = [
            ElevatedButton("Cancel", bgcolor=colors.RED_300, width=100, color="black", on_click=lambda e: self.close_form()),
            ElevatedButton("Save", bgcolor=colors.GREEN_300, width=100, color="black", on_click=lambda e: self.handle_submit()),
        ]

        self.actions = self.footer

        self.header = [Text("Add Sprint" if self.mode == "add" else "Editing Item", color="black", size=24)]

        if self.mode != "add" and self.item_dict:
            self.sprint_name.value = self.item_dict.get("sprint_name", "")
            self.status.value = self.item_dict.get("status", "")
            self.assignees = self.item_dict.get("assignee_tags", [])
            self.update_tags()

        return Container(
            content=Column(
                [
                    Row(self.header, alignment=MainAxisAlignment.SPACE_BETWEEN),
                    Row([self.sprint_name], alignment=MainAxisAlignment.SPACE_BETWEEN),

                    # Start and End date buttons
                    Row([
                        Container(self.start_date_button, padding=padding.only(0, 0, 5, 0),expand=1),
                        Container(self.end_date_button, padding=padding.only(5, 0, 0, 0),expand=1),

                        # self.start_date_button,
                        # self.end_date_button,
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    
                    Row([self.status], alignment=MainAxisAlignment.SPACE_BETWEEN),

                    Row([self.assignee_input, self.add_assignee_button]),
                    Text("Assignees:"),
                    self.tag_container,
                ],
                on_scroll=lambda e: print("Scrolled"),
                scroll=ScrollMode.AUTO,
                alignment=MainAxisAlignment.START,
            ),
            width=self.page.width * 0.4,
            height=self.page.height * 0.7,
            padding=padding.only(15, 15, 15, 15),
            border_radius=border_radius.all(10),
            expand=1
        )

    # def handle_start_date_change(self, e):
    #     self.start_date_button.text = f"Start Date: {e.control.value.strftime('%Y-%m-%d')}"
    #     self.page.update()

    # def handle_end_date_change(self, e):
    #     self.end_date_button.text = f"End Date: {e.control.value.strftime('%Y-%m-%d')}"
    #     self.page.update()

    def add_assignee(self, e):
        assignee_name = self.assignee_input.value.strip()
        if assignee_name:
            self.assignees.append(assignee_name)
            self.assignee_input.value = ""  # Clear input field after adding
            self.update_tags()  # Refresh the tag list
        self.page.update()

    def remove_assignee(self, tag):
        self.assignees.remove(tag)
        self.update_tags()
        self.page.update()

    def update_tags(self):
        self.tag_container.controls.clear()  # Clear current tags
        for assignee in self.assignees:
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

    def is_valid_form(self):
        return self.sprint_name.value != ""
    
    def handle_submit(self):
        if self.is_valid_form():
            print("Form is valid")
            item = {
                "sprint_name": self.sprint_name.value,
                "start_date": self.start_date.value,
                "end_date": self.end_date.value,
                "status": self.status.value,
                "assignees": self.assignee_input.value
            }

        else:
            print("Form submitted.")
            self.sprint_name.error_text = "Sprint name is required"
            self.page.update()
            # self.close_form()
        

# from flet import *
# from .FormComponents import DropdownInput, TextFieldInput, MultipleSelectInput
# from data.manage_data import Data
# from datetime import datetime
# import asyncio

# class SprintForm(AlertDialog):
#     def __init__(self, page, close_form, mode="add", item_dict=None):
#         print("Item form initialized")
#         super().__init__()
#         self.page = page
#         self.close_form = close_form
#         self.mode = mode  # Mode can be "add" or "view" or "edit"
#         self.item_dict = item_dict or {}
#         self.content_padding = 10
#         self.inset_padding = 10
#         self.status_options = ["Not Started", "In progress", "Completed"]
#         self.bgcolor = "#CADEED"
#         self.clip_behavior = ClipBehavior.HARD_EDGE
        
#         self.assignees = []

#         # Build the form content
#         self.content = self.build_add_sprint_form()
#         self.inset_padding = 10
#         self.actions_padding = 20

#     def build_add_sprint_form(self):
#         self.sprint_name = TextFieldInput(label="Sprint Name", is_required=True)
        
#         # self.start_date = TextFieldInput(DatePicker(
#         #     first_date=datetime(year=2023, month=10, day=1),
#         #     last_date=datetime(year=2024, month=10, day=1)),
#         # )
#         # self.end_date = TextFieldInput(DatePicker(
#         #     first_date=datetime(year=2023, month=10, day=1),
#         #     last_date=datetime(year=2024, month=10, day=1)),
#         # )

#         self.start_date_input = TextField(label="Start Date", on_focus=self.open_start_date_picker)
#         self.end_date_input = TextField(label="End Date", on_focus=self.open_end_date_picker)
        
#         self.status = Dropdown(
#             label="Status", 
#             options=[dropdown.Option(x) for x in self.status_options]
#         )

#         self.tag_container = Row(wrap=True)
#         self.assignee_input = TextField(label="Assign to: ", width=200)
#         self.add_assignee_button = ElevatedButton("Add Assignee", on_click=self.add_assignee)
#         self.assignee_tags = MultipleSelectInput(self.assignees)
#         self.task_logs = Row([Text(" ", color="black", size=15),])

#         self.footer = [
#             ElevatedButton("Cancel", bgcolor=colors.RED_300, width=100, color="black", on_click=lambda e: self.close_form()),
#             ElevatedButton("Save", bgcolor=colors.GREEN_300, width=100, color="black", on_click=lambda e: self.handle_submit()),
#         ]

#         self.actions = self.footer

#         self.header = [Text("Add Sprint" if self.mode == "add" else "Editing Item", color="black", size=24)]

#         if self.mode != "add" and self.item_dict:
#             self.sprint_name.value = self.item_dict.get("sprint_name", "")
#             self.start_date.value = self.item_dict.get("start_date", "")
#             self.end_date.value = self.item_dict.get("end_date", "")
#             self.status.value = self.item_dict.get("status", "")
#             self.assignees = self.item_dict.get("assignee_tags", [])
#             self.update_tags()

#         return Container(
#             content=Column(
#                 [
#                     Row(self.header, alignment=MainAxisAlignment.SPACE_BETWEEN),
#                     Row([self.sprint_name], alignment=MainAxisAlignment.SPACE_BETWEEN),

#                     Row([
#                         Container(self.sat, padding=padding.only(0, 0, 5, 0), expand=1),
#                         Container(self.story_points, padding=5, expand=1),
#                         Container(self.task_stage, padding=padding.only(5, 0, 0, 0), expand=1),
#                     ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    
#                     Row([
#                         Container(self.task_status, padding=padding.only(0, 0, 5, 0), expand=1),
#                         Container(self.task_type, padding=5, expand=1),
#                         Container(self.assignee, padding=padding.only(5, 0, 0, 0), expand=1),
#                     ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    
#                     Text("Tags:", color="black", size=15),
#                     Row([self.tags]),

#                     # self.task_logs,
#                     Row([
#                         Text("Logs:", color="black", size=15),
#                         Column([Container(Text(f"{log.split('T')[0]} {log.split('T')[1].split('.')[0]}", color="black")) for log in self.logs ]),
#                     ] if self.logs != [] else [], vertical_alignment=CrossAxisAlignment.START),
#                 ],
#                 on_scroll=lambda e: print("Scrolled"),
#                 scroll=ScrollMode.AUTO,
#                 alignment=MainAxisAlignment.START,
#             ),
#             # bgcolor="grey",
#             width=self.page.width * 0.4,
#             height=self.page.height * 0.7,
#             padding=padding.only(15, 15, 15, 15),
#             border_radius=border_radius.all(10),
#             expand = 1
#         )
#         # Combine all components into the form layout
#         # form_content = Column(
#         #     [
#         #         Row(self.header, alignment=MainAxisAlignment.SPACE_BETWEEN),
#         #         Row([self.sprint_name], alignment=MainAxisAlignment.SPACE_BETWEEN),

#         #         Row([
#         #             self.start_date_input,
#         #             self.end_date_input,
#         #         ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                
#         #         Row([self.status], alignment=MainAxisAlignment.SPACE_BETWEEN),

#         #         Row([self.assignee_input, self.add_assignee_button]),
#         #         Text("Assignees:"),
#         #         self.tag_container,
#         #     ],
#         #     on_scroll=lambda e: print("Scrolled"),
#         #     scroll=ScrollMode.AUTO,
#         #     alignment=MainAxisAlignment.START,

#         #     width=self.page.width * 0.4,
#         #     height=self.page.height * 0.7,
#         #     padding=padding.only(15, 15, 15, 15),
#         #     border_radius=border_radius.all(10),
#         #     expand = 1
#         # )
        
#         # return form_content


#     def open_start_date_picker(self, e):
#         # Open the date picker for the start date
#         date_picker = DatePicker(
#             first_date=datetime(year=2023, month=10, day=1),
#             last_date=datetime(year=2024, month=10, day=1),
#             on_change=self.set_start_date_value
#         )
#         self.page.dialog = AlertDialog(content=date_picker)
#         self.page.dialog.open = True
#         self.page.update()

#     def set_start_date_value(self, e):
#         # Set the selected date into the start_date_input field
#         self.start_date_input.value = e.control.value.strftime("%Y-%m-%d")
#         self.page.dialog.open = False
#         self.page.update()

#     def open_end_date_picker(self, e):
#         # Open the date picker for the end date
#         date_picker = DatePicker(
#             first_date=datetime(year=2023, month=10, day=1),
#             last_date=datetime(year=2024, month=10, day=1),
#             on_change=self.set_end_date_value
#         )
#         self.page.dialog = AlertDialog(content=date_picker)
#         self.page.dialog.open = True
#         self.page.update()

#     def set_end_date_value(self, e):
#         # Set the selected date into the end_date_input field
#         self.end_date_input.value = e.control.value.strftime("%Y-%m-%d")
#         self.page.dialog.open = False
#         self.page.update()


#     def add_assignee(self, e):
#         assignee_name = self.assignee_input.value.strip()
#         if assignee_name:
#             self.assignees.append(assignee_name)
#             self.assignee_input.value = ""  # Clear input field after adding
#             self.update_tags()  # Refresh the tag list
#         self.page.update()

#     def remove_assignee(self, tag):
#         self.assignees.remove(tag)
#         self.update_tags()
#         self.page.update()

#     def update_tags(self):
#         self.tag_container.controls.clear()  # Clear current tags
#         for assignee in self.assignees:
#             # Each tag is a Row with a label and a delete button
#             self.tag_container.controls.append(
#                 Container(
#                     content=Row(
#                         [
#                             Text(assignee),
#                             IconButton(
#                                 icon=icons.CLOSE,
#                                 on_click=lambda e, a=assignee: self.remove_assignee(a),  # Remove tag on click
#                             ),
#                         ],
#                         spacing=5,
#                     ),
#                     padding=5,
#                     border_radius=border_radius.all(8),
#                     bgcolor=colors.LIGHT_BLUE_50,  # Color the tag background
#                 )
#             )
#         self.page.update()

#     def handle_submit(self):
#         # Save logic for the sprint form
#         print("Form submitted.")
#         # Implement actual saving logic (e.g., to a database)
#         self.close_form()


