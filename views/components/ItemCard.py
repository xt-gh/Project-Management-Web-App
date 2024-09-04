from flet import *
from data.manage_data import Data

class ItemCard(Column):
    def __init__(self, item_id, handle_detailed_view=None):
        super().__init__()
        self.item_id = item_id
        self.data = Data()
        item =self.data.get_product_backlog_item(self.item_id) 

        self.task_name = item["task_name"]
        self.task_description = item["description"]
        self.priority = item["priority"]
        self.story_points = item["story_points"]
        self.tags = item["tags"]
        self.stage = item["stage"]
        self.assignee = item["assignee"]

        self.handle_detailed_view = handle_detailed_view


    def build(self):

        tags = Row()
        task_title = Text(self.task_name, color="black", size=20)
        details = Row([
            IconButton(
                icon=icons.MORE_HORIZ_ROUNDED,
                icon_color="black",
                on_click=self.handle_detailed_view
            )
        ])
        


        return Container(
            content=Column([
                            Row([
                                    Text(self.task_name, color="black", size=20),
                                    IconButton(
                                        icon=icons.MORE_HORIZ_ROUNDED,
                                        icon_color="black",
                                        on_click=self.handle_detailed_view
                                    )
                                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                            
                            ]
            ),
            bgcolor="#BABDE2",
            border=border.all(2, "#374375"),
            border_radius=border_radius.all(10),
            padding=padding.all(10),
            width=200,
            height=80,
            on_click=lambda e: print("Clickable without Ink clicked!"),
            ink=True
        )
    