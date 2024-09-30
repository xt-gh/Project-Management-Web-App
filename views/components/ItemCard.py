from flet import *

class ItemCard(Container):
    def __init__(self, item_dict, handle_detailed_view=None):
        print("Item card initialized")
        super().__init__()
        self.item_id = item_dict["_id"]
        item = item_dict

        self.task_name = item["task_name"]
        self.task_description = item["description"]
        self.priority = item["priority"]
        self.story_points = item["story_points"]
        self.tags = item["tags"]
        self.stage = item["stage"]
        self.assignee = item["assignee"]
        self.date = item["admin_add_date"]

        self.handle_detailed_view = handle_detailed_view

        self.bgcolor = "#DDDDDD"
        self.border = border.all(1.5, "#6686BD")
        self.border_radius = border_radius.all(10)
        self.padding = padding.all(10)
        self.margin = margin.all(8)
        self.expand = 1
        self.ink = True
        self.on_click = lambda e: print("Clickable without Ink clicked!")
        self.content = Column([
            self.build_tags(),
            self.card_title(),
            self.card_details()
        ])

    def build_tags(self):
        tags = Container(
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN, 
                tight=True), 
            alignment=alignment.center_left
        )
        for i in range(0, min(len(self.tags), 4)):
            tags.content.controls.append(
                Container(
                    content=Text(self.tags[i], color="black", size=12),
                    bgcolor="#FFFFFF",
                    border_radius=border_radius.all(5),
                    padding=padding.only(3, 1, 3, 1),
                    margin=margin.only(0, 0, 6, 0),
                )
                if i < 3 else
                Text(f"+{len(self.tags)-3}", color="black", size=12)
            )
        return tags

    def card_title(self):
        return Container(
            content=Text(
                self.task_name,
                color="black", 
                size=20,
                max_lines=2,
                expand=1,
                overflow=TextOverflow.ELLIPSIS
            )
        )

    def card_details(self):
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

        if self.handle_detailed_view is None:
            details.controls.pop()

        if self.story_points:
            details.controls[0].controls.insert(
                0,
                Container(Text(f"Story Points: {self.story_points} ", color="black", size=14)),
            )
            details.alignment=MainAxisAlignment.SPACE_BETWEEN

        if self.priority:
            details.controls[0].controls.insert(
                0,
                Container(Text(f"Priority: {self.priority} ", color="black", size=14)),
            )
            details.alignment=MainAxisAlignment.SPACE_BETWEEN
        return details

    # def before_update(self):
    #     print("Item card updated")
    #     self.bgcolor = "#DDDDDD"
    #     self.border = border.all(1.5, "#6686BD")
    #     self.border_radius = border_radius.all(10)
    #     self.padding = padding.all(10)
    #     self.margin = margin.all(8)
    #     self.expand = 1
    #     self.ink = True

class DraggableItemCard(Draggable):
    def __init__(self, group, item_dict, handle_drag_start, on_drag_complete, handle_detailed_view=None):
        handle_drag_start_event = lambda e: handle_drag_start(item_dict)
        self.task_name = item_dict["task_name"]
        super().__init__(
            group=group,
            content=ItemCard(item_dict, handle_detailed_view),
            on_drag_start=handle_drag_start_event,
            on_drag_complete=on_drag_complete
        )