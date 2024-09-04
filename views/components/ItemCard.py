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

        tags = Container(
            content=Row(
                alignment=MainAxisAlignment.START, 
                wrap=False), 
            bgcolor="#CADEED", 
            alignment=alignment.center_left
        )
        for tag in self.tags:
            tags.content.controls.append(
                Container(
                    content=Text(tag, color="black", size=12),
                    bgcolor="#F1F1F1",
                    border_radius=border_radius.all(5),
                    padding=padding.all(1),
                    margin=margin.all(2),
                )
            )
        task_title = Container(
            content=Text(
                self.task_name,
                color="black", 
                size=20,
                max_lines=2,
                overflow=TextOverflow.ELLIPSIS
            ),
            bgcolor="#CADEED",
        )
            
        details = Row([
            Column(),
            IconButton(
                icon=icons.MORE_HORIZ_ROUNDED,
                icon_color="black",
                icon_size=20,
                on_click=lambda e: self.handle_detailed_view(self.item_id),
                hover_color="#F1F1F1",

            )
        ], 
        alignment=MainAxisAlignment.END,
        # tight=True,
        )

        if self.story_points:
            details.controls[0].controls.insert(
                0,
                Container(Text(f"  Story Points: {self.story_points} ", color="black", size=12), bgcolor="#CADEED"),
            )
            details.alignment=MainAxisAlignment.SPACE_BETWEEN

        if self.priority:
            details.controls[0].controls.insert(
                0,
                Container(Text(f"Priority: {self.priority} ", color="black", size=12), bgcolor="#CADEED"),
            )
            details.alignment=MainAxisAlignment.SPACE_BETWEEN


        return Container(
            content=Column([
                tags,
                task_title,
                details
            ]
            ),
            bgcolor="#BABDE2",
            border=border.all(2, "#374375"),
            border_radius=border_radius.all(10),
            padding=padding.all(10),
            width=200,
            on_click=lambda e: print("Clickable without Ink clicked!"),
            ink=True
        )
    