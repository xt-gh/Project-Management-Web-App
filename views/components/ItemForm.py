from flet import *
from .FormComponents import DropdownInput, TextFieldInput
from .ItemCard import ItemCard

class ItemForm(Column):
    def __init__(self, data, page, close_form):
        super().__init__()
        self.data = data
        self.page = page
        self.close_form = close_form
        self.fibbonacci = [0, 0.5, 1, 2, 3, 5, 8, 13, 20, 40, 100]
        self.stages = ["Planning", "Development", "Testing", "Implementation"]
        self.tags = ["Front-end", "Back-end", "API", "Database", "UI", "UX", "Testing", "Framework"]
        self.priotities = ["Low", "Medium", "Important", "Urgent"]
        self.users = ["John Doe", "Jane Doe", "John Smith", "Jane Smith"]

    
    def build(self):
        self.task_name = TextFieldInput()
        self.task_description = TextFieldInput()
        self.priority = DropdownInput(self.priotities)
        self.story_points = DropdownInput(self.fibbonacci)
        # self.type = TextFieldInput()
        self.tags = DropdownInput(self.tags)
        self.stage = DropdownInput(self.stages)
        self.assignee = DropdownInput(self.users)
        

        return Container(
            content=Column([
            Text("Add Item", color="black", size=24),
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
                # Row([
                #     Text("Type: ", color="black", size=20, width=150),
                #     self.type,
                # ], alignment=MainAxisAlignment.SPACE_BETWEEN),
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
                    ElevatedButton("Submit", bgcolor="#DAE9FE", color="black", on_click=lambda e: self.close_form()),
                    ElevatedButton("Cancel", bgcolor="#DAE9FE", color="black", on_click=lambda e: self.close_form()),
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
            ]),
            bgcolor="grey",
            width=self.page.width * 0.5,
            height=self.page.height * 0.85,
            padding=padding.all(15),
            border_radius=border_radius.all(10),
        )
    
    def handle_submit(self):
        return ItemCard(
            task_name=self.task_name.value,
            task_description=self.task_description.value,
            priority=self.priority.value,
            story_points=self.story_points.value,
            tags=self.tags.value,
            stage=self.stage.value,
            assignee=self.assignee.value
        )