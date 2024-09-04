from flet import *
from .FormComponents import DropdownInput, TextFieldInput, MultipleSelectInput
from .ItemCard import ItemCard
from data.manage_data import Data

class ItemForm(Column):
    def __init__(self, page, close_form, mode="add", id=None):
        super().__init__()
        self.page = page
        self.close_form = close_form
        self.mode = mode # Mode can be "add" or "view" or "edit"
        self.item_id = id
        self.product_backlog_items = Data()

        self.fibbonacci = [0, 0.5, 1, 2, 3, 5, 8, 13, 20, 40, 100]
        self.stages = ["Planning", "Development", "Testing", "Implementation"]
        self.tags = ["Front-end", "Back-end", "API", "Database", "UI", "UX", "Testing", "Framework"]
        self.priotities = ["Low", "Medium", "Important", "Urgent"]
        self.users = ["John Doe", "Jane Doe", "John Smith", "Jane Smith"]
        self.header = []

    
    def build(self):
        # if self.data
        self.task_name = TextFieldInput(is_required=True)
        self.task_description = TextFieldInput()
        self.task_description.multiline = True
        self.priority = DropdownInput(self.priotities)
        self.story_points = DropdownInput(self.fibbonacci)
        self.tags = MultipleSelectInput(self.tags)
        self.stage = DropdownInput(self.stages)
        self.assignee = MultipleSelectInput(self.users)

        if self.mode == "view" or self.mode == "edit":
            item = self.product_backlog_items.get_product_backlog_item(self.item_id)
            self.task_name.value = item["task_name"]
            self.task_description.value = item["description"]
            self.priority.value = item["priority"]
            self.story_points.value = item["story_points"]
            self.stage.value = item["stage"]
            self.assignee.value = item["assignee"]

            editable = (self.mode == "edit")

            self.task_name.disabled = not editable
            self.task_description.disabled = not editable


        return Container(
            content=Column([
                Row([
                    Text("Add Item", color="black", size=24),
                    # self.header,
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Row([
                    Text("Task Name: ", color="black", size=20, width=150),
                    self.task_name,
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Row([
                    Text("Description: ", color="black", size=20, width=150),
                    self.task_description,
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Row([
                    Text("Priority: ", color="black", size=20, width=150),
                    self.priority,
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Row([
                    Text("Story Points: ", color="black", size=20, width=150),
                    self.story_points,
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Row([
                    Text("Tags: ", color="black", size=20, width=150),
                    self.tags,
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Row([
                    Text("Stage: ", color="black", size=20, width=150),
                    self.stage,
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Row([
                    Text("Assignee: ", color="black", size=20, width=150),
                    self.assignee,
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Row([
                    ElevatedButton("Save", bgcolor="#DAE9FE", color="black", on_click=lambda e: self.handle_submit()),
                    ElevatedButton("Cancel", bgcolor="#DAE9FE", color="black", on_click=lambda e: self.close_form()),
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
            ],
            on_scroll=lambda e: print("Scrolled"),
            scroll=ScrollMode.AUTO,
            ),
            bgcolor="pink",
            width=self.page.width * 0.5,
            height=self.page.height * 0.85,
            padding=padding.all(15),
            border_radius=border_radius.all(10),
        )
    
    def is_valid_form(self):
        return self.task_name.value != ""
    
    def handle_submit(self):
        if self.is_valid_form():
            print("Form is valid")
            item = "new item"
            # self.data.append(item)
            self.product_backlog_items.add_product_backlog_item(
                task_name=self.task_name.value,
                description=self.task_description.value,
                priority=self.priority.value,
                story_points=self.story_points.value,
                tags=self.tags.selected_options,
                stage=self.stage.value,
                assignee=self.assignee.selected_options
            )
            print("Added new item:", self.product_backlog_items.get_product_backlog_items())
            self.close_form()
            self.page.update()
        
        else:
            print("Form is invalid")
            self.task_name.error_text = "Task name is required"
            self.page.update()