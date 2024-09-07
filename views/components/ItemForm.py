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

        self.fibbonacci = [0, 0.5, 1, 2, 3, 5, 8, 13, 20, 40, 100]
        self.stage_options = ["Planning", "Development", "Testing", "Implementation"]
        self.tag_options = ["Front-end", "Back-end", "API", "Database", "UI", "UX", "Testing", "Framework"]
        self.priotity_options = ["Low", "Medium", "Important", "Urgent"]
        self.users = ["John Doe", "Jane Doe", "John Smith", "Jane Smith"]
        self.header = []
        
        self.bgcolor = "#CADEED"
        self.clip_behavior = ClipBehavior.HARD_EDGE
        
        self.content = self.build_add_item_form() 
        
    def build_add_item_form(self):
        self.task_name = TextFieldInput(is_required=True)
        self.task_description = TextFieldInput()
        self.task_description.multiline = True
        self.task_description.min_lines = 3
        self.priority = DropdownInput(self.priotity_options)
        self.story_points = DropdownInput(self.fibbonacci)
        self.tags = MultipleSelectInput(self.tag_options)
        self.stage = DropdownInput(self.stage_options)
        self.assignee = MultipleSelectInput(self.users)
        self.footer = [
            ElevatedButton("Cancel", bgcolor="#DAE9FE", color="black", on_click=lambda e: self.close_form()),
            ElevatedButton("Save", bgcolor="#DAE9FE", color="black", on_click=lambda e: self.handle_submit()),
            
        ]

        if self.mode == "add":
            self.header = [Text("Add Item", color="black", size=24)]

        else:
            self.header = [
                Text("Editing Item", color="#F5F5F5", size=24),
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

            for user in item["assignee"]:
                self.assignee.handle_add_tag(user)
        
        title_to_form = [
            ("Task Name", self.task_name),
            ("Description", self.task_description),
            ("Priority", self.priority),
            ("Story Points", self.story_points),
            ("Tags", self.tags),
            ("Stage", self.stage),
            ("Assignee", self.assignee),
        ]
    
        return Container(
            content=Column(
                [Row(self.header, alignment=MainAxisAlignment.SPACE_BETWEEN)] +
                [Row(
                    controls=[Text(title, color="#F5F5F5", size=20, width=150), form], 
                    alignment=MainAxisAlignment.SPACE_BETWEEN, 
                    vertical_alignment=CrossAxisAlignment.START) 
                    for title, form in title_to_form] +
                [Row (self.footer, alignment=MainAxisAlignment.SPACE_BETWEEN)],
                #     Row(self.header, alignment=MainAxisAlignment.SPACE_BETWEEN),
                #     Row([
                #         Text("Task Name: ", color="black", size=20, width=150),
                #         self.task_name,
                #     ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                #     Row([
                #         Text("Description: ", color="black", size=20, width=150),
                #         self.task_description,
                #     ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                #     Row([
                #         Text("Priority: ", color="black", size=20, width=150),
                #         self.priority,
                #     ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                #     Row([
                #         Text("Story Points: ", color="black", size=20, width=150),
                #         self.story_points,
                #     ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                #     Row([
                #         Text("Tags: ", color="black", size=20, width=150),
                #         self.tags,
                #     ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                #     Row([
                #         Text("Stage: ", color="black", size=20, width=150),
                #         self.stage,
                #     ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                #     Row([
                #         Text("Assignee: ", color="black", size=20, width=150),
                #         self.assignee,
                #     ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                #     Row([
                #         ElevatedButton("Save", bgcolor="#DAE9FE", color="black", on_click=lambda e: self.handle_submit()),
                #         ElevatedButton("Cancel", bgcolor="#DAE9FE", color="black", on_click=lambda e: self.close_form()),
                #     ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                # ],
                on_scroll=lambda e: print("Scrolled"),
                scroll=ScrollMode.AUTO,
            ),
            bgcolor="#6686BD",
            width=self.page.width * 0.5,
            height=self.page.height * 0.85,
            padding=padding.all(10),
            border_radius=border_radius.all(10),
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
    