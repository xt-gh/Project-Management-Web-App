from flet import *

class ItemCard(Row):
    def __init__(self, task_name="test", task_description="", priority="", story_points="", tags="", stage="", assignee="", *args, **kwargs):
        super().__init__()
        self.task_name = task_name
        self.task_description = task_description
        self.priority = priority
        self.story_points = story_points
        self.tags = tags
        self.stage = stage
        self.assignee = assignee


    def build(self):
        return Container(
            content=Row([
                Text(self.task_name, color="black", size=16),
                IconButton(
                    icon=icons.MORE_HORIZ_ROUNDED,
                    icon_color="black"
                )
            ]),
            bgcolor="#BABDE2",
            border=border.all(2, "#374375"),
            border_radius=border_radius.all(10),
            padding=padding.all(10),
            on_click=lambda e: print("Clickable without Ink clicked!"),
            ink=True
        )
    