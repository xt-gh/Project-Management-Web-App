from flet import *
from .FormComponents import DropdownInput, TextFieldInput, MultipleSelectInput
from data.manage_data import Data

class ItemForm(AlertDialog):
    def __init__(self, page, close_form, mode="add", id=None):
        super().__init__()
        self.page = page
        self.close_form = close_form
        self.mode = mode # Mode can be "add" or "view" or "edit"
        self.item_id = id
        self.product_backlog_items = Data()
        self.content_padding = 10

        # self.inset_padding = 10

        self.fibbonacci = [0, 0.5, 1, 2, 3, 5, 8, 13, 20, 40, 100]
        self.stage_options = ["Planning", "Development", "Testing", "Implementation"]
        self.tag_options = ["Front-end", "Back-end", "API", "Database", "UI", "UX", "Testing", "Framework"]
        self.priotity_options = ["Low", "Medium", "Important", "Urgent"]
        self.users = ["John Doe", "Jane Doe", "John Smith", "Jane Smith"]
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
        self.task_type = DropdownInput(self.task_type_options, label="Type")
        self.tags = MultipleSelectInput(self.tag_options)
        self.assignee = TextFieldInput(label="Assignee", expand=False)
        self.footer = [
            ElevatedButton("Cancel", bgcolor=colors.GREY_400, width=100, color="black", on_click=lambda e: self.close_form()),
            ElevatedButton("Save", bgcolor=colors.RED_300, width=100, color="black", on_click=lambda e: self.handle_submit()),
        ]

        self.actions = self.footer

        if self.mode == "add":
            self.header = [Text("Add Item", color="black", size=24)]

        else:
            self.header = [
                Text("Editing Item", color="black", size=24),
                IconButton(
                    icon=icons.DELETE_FOREVER,
                    icon_color="black",
                    on_click=lambda e: print("Delete clicked"),
                )
            ]

            item = self.product_backlog_items.get_product_backlog_item(self.item_id)

            self.task_name.value = item["task_name"]
            self.task_description.value = item["description"]
            self.priority.value = item["priority"]
            self.story_points.value = item["story_points"]
            self.stage.value = item["stage"]
            
            for tag in item["tags"]:
                self.tags.handle_add_tag(tag)
    
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
                    
                    Text("Tags:", color="black", size=15),
                    Column([self.tags], alignment=MainAxisAlignment.SPACE_BETWEEN),
                ],
                on_scroll=lambda e: print("Scrolled"),
                scroll=ScrollMode.AUTO,
                alignment=MainAxisAlignment.START,
            ),
            # bgcolor="grey",
            width=self.page.width * 0.4,
            height=self.page.height * 0.7,
            padding=padding.only(15, 15, 15, 15),
            border_radius=border_radius.all(10),
            expand = 1
        )
    
    def is_valid_form(self):
        return self.task_name.value != ""
    
    def handle_submit(self):
        if self.is_valid_form():
            print("Form is valid")
            item = {
                "task_name": self.task_name.value,
                "description": self.task_description.value,
                "priority": self.priority.value,
                "story_points": self.story_points.value,
                "tags": self.tags.selected_options,
                "stage": self.stage.value,
                "assignee": self.assignee.selected_options
            }
            if self.mode == "add":
                self.product_backlog_items.add_product_backlog_item(item)
                print("Added new item:", self.product_backlog_items.get_product_backlog_items())

            if self.mode == "view":
                self.product_backlog_items.update_product_backlog_item(id=self.item_id, item=item)
                print("Updated item:", self.product_backlog_items.get_product_backlog_item(id=self.item_id))
            self.close_form()
            self.page.update()
        
        else:
            print("Form is invalid")
            self.task_name.error_text = "Task name is required"
            self.page.update()
    