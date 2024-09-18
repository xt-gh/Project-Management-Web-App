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
        self.start_date_value = ""
        self.end_date_value = ""

        # Build the form content
        self.content = self.build_add_sprint_form()
        self.inset_padding = 10
        self.actions_padding = 20

    def build_add_sprint_form(self):
        self.sprint_name = TextFieldInput(label="Sprint Name", is_required=True)
    
       # Start date field with focus event to trigger DatePicker
        self.start_date_field = TextField(
            label="Start Date",
            hint_text="YYYY-MM-DD",
            read_only=True,
            # on_focus=self.open_start_date_picker
        )

        # End date field with focus event to trigger DatePicker
        self.end_date_field = TextField(
            label="End Date",
            hint_text="YYYY-MM-DD",
            read_only=True,

            # on_focus=self.open_end_date_picker
        )

        self.status = Dropdown(
            label="Status", 
            options=[dropdown.Option(x) for x in self.status_options]
        )

        self.tag_container = Row(wrap=True)
        self.assignee_input = TextField(label="Assign to: ", width=200)
        self.add_assignee_button = ElevatedButton(icon="add", text="Add Assignee", on_click=self.add_assignee)
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

                    Row([
                        Container(self.start_date_field, width=150, padding=padding.only(0, 0, 5, 0), expand=1),
                        Container(ElevatedButton("Pick Start Date",icon="date_range", on_click=self.open_start_date_picker)),
                        # Container(self.end_date_field, width=100, padding=padding.only(5, 0, 0, 0), expand=1),
                        # Container(ElevatedButton("Pick End Date", icon="date_range", on_click=self.open_end_date_picker)),
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),

                    Row([
                        Container(self.end_date_field,width=150, padding=padding.only(0, 0, 5, 0), expand=1),
                        Container(ElevatedButton("Pick End Date",icon="date_range", on_click=self.open_end_date_picker)),
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

    def open_start_date_picker(self, e):
        self.page.dialog = DatePicker(
            first_date=datetime(2015, 1, 1),
            last_date=datetime(2032, 12, 31),
            on_change=self.set_start_date,
            on_dismiss=self.handle_start_date_dismissal
        )
        self.page.dialog.open = True
        self.page.update()

    def handle_start_date_dismissal(self, e):
        # Clear the dialog after dismissing
        self.page.dialog = None
        self.page.update()

    def set_start_date(self, e):
        if e.control.value:
            self.start_date_field.value = e.control.value.strftime("%Y-%m-%d")
        # Clear the dialog after setting the date
        self.page.dialog = None
        self.page.update()

    def open_end_date_picker(self, e):
        self.page.dialog = DatePicker(
            first_date=datetime(2015, 1, 1),
            last_date=datetime(2032, 12, 31),
            on_change=self.set_end_date,
            on_dismiss=self.handle_end_date_dismissal
        )
        self.page.dialog.open = True
        self.page.update()

    def handle_end_date_dismissal(self, e):
        # Clear the dialog after dismissing
        self.page.dialog = None
        self.page.update()

    def set_end_date(self, e):
        if e.control.value:
            self.end_date_field.value = e.control.value.strftime("%Y-%m-%d")
        # Clear the dialog after setting the date
        self.page.dialog = None
        self.page.update()


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
                "start_date": self.start_date_field.value,
                "end_date": self.end_date_field.value,
                "status": self.status.value,
                "assignees": self.assignee_input.value
            }
            self.close_form()

        else:
            print("Form submitted.")
            self.sprint_name.error_text = "Sprint name is required"
            self.page.update()
  

