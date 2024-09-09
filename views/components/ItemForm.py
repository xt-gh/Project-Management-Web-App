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
        self.task_stage_options = ["Planning", "Development", "Testing", "Implementation"]
        self.task_status_options = ["Not Started", "In Progress", "Completed"]
        self.task_type_options = ["User Story", "Bug"]
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
        self.task_stage = DropdownInput(self.task_stage_options)
        self.task_status = DropdownInput(self.task_status_options)
        self.task_type = DropdownInput(self.task_type_options)
        self.tags = MultipleSelectInput(self.tag_options)
        self.assignee = TextFieldInput()
        self.footer = [
            ElevatedButton("Cancel", bgcolor="#DAE9FE", width=100, color="black", on_click=lambda e: self.close_form()),
            ElevatedButton("Save", bgcolor="#DAE9FE", width=100, color="black", on_click=lambda e: self.handle_submit()),
        ]

        if self.mode == "add":
            self.header = [Text("Add Item", color="white", size=24)]

        else:
            self.header = [
                Text("Editing Item", color="white", size=24),
                IconButton(
                    icon=icons.DELETE_FOREVER,
                    icon_color="white",
                    on_click=lambda e: print("Delete clicked"),
                )
            ]

            item = self.product_backlog_items.get_product_backlog_item(self.item_id)

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

        # Give each form element a label
        self.task_name.label = "Task Name"
        self.task_description.label = "Description"
        self.priority.label = "Priority"
        self.story_points.label = "Story Points"
        self.task_stage.label = "Stage"
        self.task_status.label = "Status"
        self.task_type.label = "Type"
        self.assignee.label = "Assignee"
        
        title_to_form = [
            ("Task Name", self.task_name),
            ("Description", self.task_description),
            ("Priority", self.priority),
            ("Story Points", self.story_points),
            ("Stage", self.task_stage),
            ("Status", self.task_status),
            ("Type", self.task_type),
            ("Tags", self.tags),
            ("Assignee", self.assignee),
        ]
    
        return Container(
            content=Column(
                [Row(self.header, alignment=MainAxisAlignment.SPACE_BETWEEN)] +
                [Row(
                    # controls=[Container(Text(title, color="black", size=20, width=150), margin=margin.all(5)), form], 
                    controls=[form], 
                    alignment=MainAxisAlignment.SPACE_BETWEEN, 
                    vertical_alignment=CrossAxisAlignment.START) 
                    for title, form in title_to_form] +
                [Container(Row (self.footer, alignment=MainAxisAlignment.END), padding=padding.only(0, 0, 0, 10))],
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
            # bgcolor="grey",
            width=self.page.width * 0.5,
            height=self.page.height * 0.85,
            padding=padding.only(15, 15, 15, 15),
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
                "stage": self.task_stage.value,
                "status": self.task_status.value,
                "type": self.task_type.value,
                "tags": self.tags.selected_options,
                "assignee": self.assignee.value
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
    