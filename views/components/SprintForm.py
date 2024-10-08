import asyncio
import asyncio
from flet import *
from .FormComponents import DropdownInput, TextFieldInput, MultipleSelectInput, TextFieldDatePicker
from data.manage_data import Data
from data.manage_sprint_data import SprintData
from data.manage_sprint_data import SprintData
from datetime import datetime

class SprintForm(AlertDialog):
    def __init__(self, page, close_form, mode="add", sprint_dict=None):
        print("Item form initialized")
        super().__init__()
        self.page = page
        self.close_form = close_form
        self.mode = mode  # Mode can be "add" or "view" or "edit"
        self.sprint_dict = sprint_dict
        self.sprint_dict = sprint_dict
        self.content_padding = 10
        self.inset_padding = 10
        self.status_options = ["Not Started", "In progress", "Completed"]
        self.bgcolor = "#CADEED"
        self.clip_behavior = ClipBehavior.HARD_EDGE
        
        
        # Build the form content
        self.content = self.build_add_sprint_form()
        self.inset_padding = 10
        self.actions_padding = 20
    
    def build_add_sprint_form(self):
        self.sprint_name = TextFieldInput(label="Sprint Name", is_required=True)
        self.product_owner = DropdownInput(label="Product Owner", options=["KX", "JN", "JX"], is_required=True)
        self.scrum_master = DropdownInput(label="Scrum Master", options=["KX", "JN", "JX"], is_required=True)
        self.scrum_team = MultipleSelectInput(["KX", "JN", "JX"])
        self.start_date = TextFieldDatePicker(page=self.page, label="Start Date", is_required=True)
        self.end_date = TextFieldDatePicker(page=self.page, label="End Date", is_required=True)

        self.actions = [
            ElevatedButton("Cancel", bgcolor=colors.RED_300, width=100, color="black", on_click=lambda e: self.close_form()),
            ElevatedButton("Save", bgcolor=colors.GREEN_300, width=100, color="black", on_click=lambda e: self.handle_submit()),
        ]

        if self.mode == "add":
            self.header = [Text("Add Sprint" if self.mode == "add" else "Editing Item", color="black", size=24)]
        if self.mode == "add":
            self.header = [Text("Add Sprint" if self.mode == "add" else "Editing Item", color="black", size=24)]

        else:
            self.header = [
                Text("Editing Sprint", color="black", size=24),
                IconButton(
                    icon=icons.DELETE_FOREVER,
                    icon_color="black",
                    on_click=lambda e: (asyncio.run(SprintData().remove_sprint_item(self.sprint_dict["_id"])), self.close_form()),
                )
            ]

            self.sprint_name.value = self.sprint_dict["sprint_name"]
            self.product_owner.value = self.sprint_dict["product_owner"]
            self.scrum_master.value = self.sprint_dict["scrum_master"]
            self.start_date.set_date(self.sprint_dict["start_date"])
            self.end_date.set_date(self.sprint_dict["end_date"])

            
            for member in self.sprint_dict["scrum_team"]:
                self.scrum_team.handle_add_tag(member)


        return Container(
            content=Column(
                [
                    Row(self.header, alignment=MainAxisAlignment.SPACE_BETWEEN),
                    # self.sprint_name,
                    # self.sprint_name,
                    Row([self.sprint_name], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    # Row([self.product_owner, self.scrum_master], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    self.product_owner,
                    self.scrum_master,
                    Text("Scrum team:", color="black", size=15),
                    Row([self.scrum_team]),

                    self.start_date,
                    self.end_date,

                ],
                on_scroll=lambda e: print("Scrolled"),
                scroll=ScrollMode.AUTO,
                alignment=MainAxisAlignment.START,
            ),
            width=self.page.width * 0.3,
            height=self.page.height * 0.6,
            padding=padding.only(15, 15, 15, 15),
            border_radius=border_radius.all(10),
            expand=1
        )

    def is_valid_form(self):
        is_valid = True
        if self.sprint_name.value.strip() == "":
            is_valid = False

        if self.product_owner.value == "":
            is_valid = False
        
        if self.scrum_master.value == "":
            is_valid = False
        
        if self.start_date.value == "":
            is_valid = False
        
        if self.end_date.value == "":
            is_valid = False

        if self.are_dates_valid() is not True:
            is_valid = False

        return is_valid
    
    def are_dates_valid(self):
        if self.start_date.value == "":
            return "Start date is required"
        if self.end_date.value == "":
            return "End date is required"

        start_date_components = self.start_date.value.split("-")
        end_date_components = self.end_date.value.split("-")

        today_date_components = datetime.now().strftime('%d-%m-%Y').split("-")
        # Make sure the start date is not in the past
        if int(start_date_components[2]) < int(today_date_components[2]):
            return "Start date is in the past"
        elif int(start_date_components[2]) == int(today_date_components[2]):
            if int(start_date_components[1]) < int(today_date_components[1]):
                return "Start date is in the past"
            elif int(start_date_components[1]) == int(today_date_components[1]):
                if int(start_date_components[0]) < int(today_date_components[0]):
                    return "Start date is in the past"

        # Make sure the start date is before the end date
        if int(start_date_components[2]) > int(end_date_components[2]):
            return "End date should be after start date"
        elif int(start_date_components[2]) == int(end_date_components[2]):
            if int(start_date_components[1]) > int(end_date_components[1]):
                return "End date should be after start date"
            elif int(start_date_components[1]) == int(end_date_components[1]):
                if int(start_date_components[0]) >= int(end_date_components[0]):
                    return "End date should be after start date"
        
        return True
    def is_valid_form(self):
        is_valid = True
        if self.sprint_name.value.strip() == "":
            is_valid = False

        if self.product_owner.value == "":
            is_valid = False
        
        if self.scrum_master.value == "":
            is_valid = False
        
        if self.start_date.value == "":
            is_valid = False
        
        if self.end_date.value == "":
            is_valid = False

        if self.are_dates_valid() is not True:
            is_valid = False

        return is_valid
    
    def handle_submit(self):
        if self.is_valid_form():
            print("Form is valid")
            sprint = {
                "sprint_name": self.sprint_name.value,
                "product_owner": self.product_owner.value,
                "scrum_master": self.scrum_master.value,
                "scrum_team": self.scrum_team.selected_options,
                "product_owner": self.product_owner.value,
                "scrum_master": self.scrum_master.value,
                "scrum_team": self.scrum_team.selected_options,
                "start_date": self.start_date.value,
                "end_date": self.end_date.value,
            }

            if self.mode == "add":
                asyncio.run(SprintData().add_sprint_item(sprint))
            
            else:
                # sprint["_id"] = self.sprint_dict["_id"]
                asyncio.run(SprintData().update_sprint_item(sprint_id=self.sprint_dict["_id"], updated_fields=sprint))
            self.close_form()

        else:

            if self.sprint_name.value.strip() == "":
                self.sprint_name.error_text = "Sprint name is required"
            if self.product_owner.value == "":
                self.product_owner.error_text = "Product owner is required"
            if self.scrum_master.value == "":
                self.scrum_master.error_text = "Scrum master is required"
            if self.start_date.value == "":
                self.start_date.content.controls[1].error_text = "Start date is required"
            if self.end_date.value == "":
                self.end_date.content.controls[1].error_text = "End date is required"
            
            if self.are_dates_valid() is not True:
                date_error_message = self.are_dates_valid()
                if date_error_message.startswith("Start"):
                    self.start_date.content.controls[1].error_text = date_error_message
                elif date_error_message.startswith("End"):
                    self.end_date.content.controls[1].error_text = date_error_message
            self.page.update()