from flet import *
from .FormComponents import DropdownInput, TextFieldInput, MultipleSelectInput
from data.manage_data import Data
from datetime import datetime
import asyncio

class ItemFormInSprint(AlertDialog):
    def __init__(self, page, close_form, mode="add", item_dict=None):
        print("Item form initialized")
        super().__init__()
        self.page = page
        self.close_form = close_form
        self.mode = mode # Mode can be "add" or "view" or "edit"
        self.item_dict = item_dict
        # self.data = Data()
        self.content_padding = 10

        self.inset_padding = 10

        self.priotity_options = ["Low", "Medium", "Important", "Urgent"]
        self.fibbonacci = [0, 0.5, 1, 2, 3, 5, 8, 13, 20, 40, 100]
        self.task_stage_options = ["Planning", "Development", "Testing", "Implementation"]
        self.task_status_options = ["Not Started", "In Progress", "Completed"]
        self.task_type_options = ["User Story", "Bug"]
        self.tag_options = ["Front-end", "Back-end", "API", "Database", "UI", "UX", "Testing", "Framework"]
        self.logs = []
        self.header = []
        
        self.bgcolor = "#CADEED"
        self.clip_behavior = ClipBehavior.HARD_EDGE
        
        self.content = self.build_add_item_form() 
        self.inset_padding = 10
        self.actions_padding = 20
        
    def build_add_item_form(self):
        self.task_name = TextFieldInput(label="Task Name", is_required=True)
        self.task_description = TextFieldInput(label="Description")
        self.task_description.multiline = True
        self.task_description.min_lines = 3
        self.priority = DropdownInput(self.priotity_options, label="Priority")
        self.story_points = DropdownInput(self.fibbonacci, label="Story Points")
        self.task_stage = DropdownInput(self.task_stage_options, label="Stage")
        self.task_status = DropdownInput(self.task_status_options, label="Status")
        self.task_status.disabled = True
        self.task_type = DropdownInput(self.task_type_options, label="Type")
        self.assignee = TextFieldInput(label="Assignee", is_required=True, expand=False)
        self.tags = MultipleSelectInput(self.tag_options)

        
        self.chart = Container(Text("Chart goes here"), padding=padding.all(10), bgcolor="#FFFFFF", border_radius=border_radius.all(10))

        self.task_logs = Row([Text(" ", color="black", size=15),])


        self.actions = [
            ElevatedButton("Cancel", bgcolor=colors.RED_300, width=100, color="black", on_click=lambda e: self.close_form()),
            ElevatedButton("Save", bgcolor=colors.GREEN_300, width=100, color="black", on_click=lambda e: self.handle_submit()),
        ]

        self.header = [
            Text("Editing Item", color="black", size=24),
            IconButton(
                icon=icons.DELETE_FOREVER,
                icon_color="black",
                on_click=lambda e: (asyncio.run(Data().remove_product_backlog_item(self.item_dict["_id"])), self.close_form()),
            )
        ]

        # item = asyncio.run(self.data.get_product_backlog_item(self.item_id))
        item = self.item_dict

        self.task_name.value = item["task_name"]
        self.task_description.value = item["description"]
        self.priority.value = item["priority"]
        self.story_points.value = item["story_points"]
        self.task_stage.value = item["stage"]
        self.task_status.value = item["status"]
        self.task_type.value = item["type"]
        self.assignee.value = item["assignee"]
        
        for tag in item["tags"]:
            self.tags.handle_add_tag(tag)
        
        self.logs = item["logs"]

        # self.task_logs = 
    
        return Container(
            content=Column(
                [
                    Row(self.header, alignment=MainAxisAlignment.SPACE_BETWEEN),
                    Row([self.task_name], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    Row([self.task_description], alignment=MainAxisAlignment.SPACE_BETWEEN),

                    Row([
                        Container(self.priority, padding=padding.only(0, 0, 5, 0), expand=1),
                        Container(self.story_points, padding=5, expand=1),
                        Container(self.task_stage, padding=padding.only(5, 0, 0, 0), expand=1),
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    
                    Row([
                        Container(self.task_status, padding=padding.only(0, 0, 5, 0), expand=1),
                        Container(self.task_type, padding=5, expand=1),
                        Container(self.assignee, padding=padding.only(5, 0, 0, 0), expand=1),
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    
                    Row([Text("Tags:", color="black", size=15)]),
                    Row([self.tags]),

                    self.chart,
                    ElevatedButton("Add time record", icon="add", on_click=lambda e: print("Add time record clicked")),
                    # Row([self.chart]),

                    # self.task_logs,
                    Row([
                        Text("Logs:", color="black", size=15),
                        Column(
                            [
                                Container(
                                    Text(log, color="black"),
                                    # Text(f"{log.split('T')[0]} {log.split('T')[1].split('.')[0]}", color="black")
                                ) for log in self.logs
                            ]
                        ),
                        ] if self.logs != [] else [],
                        vertical_alignment=CrossAxisAlignment.START
                    ),
                ],
                on_scroll=lambda e: print("Scrolled"),
                scroll=ScrollMode.AUTO,
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
            # bgcolor="grey",
            width=self.page.width * 0.4,
            height=self.page.height * 0.7,
            padding=padding.only(15, 15, 15, 15),
            border_radius=border_radius.all(10),
            expand = 1
        )
    
    def is_valid_form(self):
        is_valid = True
        if self.task_name.value.strip() == "":
            is_valid = False
        if self.assignee.value.strip() == "":
            is_valid = False
        return is_valid
    
    def handle_submit(self):
        if self.is_valid_form():
            print("Form is valid")
            item = {
                "task_name": self.task_name.value,
                "description": self.task_description.value,
                "priority": self.priority.value,
                "story_points": self.story_points.value,
                "stage": self.task_stage.value,
                "status": self.task_status.value,
                "type": self.task_type.value,
                "assignee": self.assignee.value,
                "tags": self.tags.selected_options,
                "time_accumulation": [],
            }

            item["logs"] = self.logs
            item["logs"].append("Item updated on " + datetime.utcnow().isoformat())
            asyncio.run(Data().update_product_backlog_item(item_id=self.item_dict["_id"], updated_fields=item))
            self.close_form()
        
        else:
            print("Form is invalid")
            if self.task_name.value == "":
                self.task_name.error_text = "Task name is required"
            if self.assignee.value == "":
                self.assignee.error_text = "An assignee is required"
            self.page.update()
    