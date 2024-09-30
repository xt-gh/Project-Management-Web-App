import asyncio
from datetime import datetime
from flet import *
from data.manage_data import Data
from data.manage_sprint_data import SprintData
from views.components.ItemCard import ItemCard, DraggableItemCard
from views.components.LoadingCard import LoadingCard

class SprintBacklogView(Column):
    def __init__(self, page):
        super().__init__()
        print("Sprint backlog initialized")
        self.page = page

        self.bgcolor = "#CADEED"
        self.padding = padding.all(15)
        self.border_radius = border_radius.all(10)
        self.drag_source = None
        self.drag_target = None

    def build_product_backlog_column(self, product_backlog_items=None):
        
        if product_backlog_items == []:
            body = Container(
                content=Column([
                    Text("No items in the product backlog", color=colors.BLACK, size=20)
                ], alignment=MainAxisAlignment.CENTER),
                expand=1,
            )

        elif product_backlog_items:
            body = Container(
                content=Column(
                    [],
                    alignment=MainAxisAlignment.CENTER,
                    scroll=ScrollMode.AUTO,
                    on_scroll=lambda e: print("Scrolled"),
                ),
                expand=1,
            )

            for product_backlog_item in product_backlog_items:
                body.content.controls.append(
                    DraggableItemCard(
                        group="backlog",
                        item_dict=product_backlog_item,
                        handle_drag_start=self.set_drag_source,
                        on_drag_complete=lambda e: self.reset_drag_source(),
                    )
                )
                body.content.controls.sort(key=lambda x: x.task_name)
        
        else:
            body = LoadingCard("Retrieving Product Backlog Items...")

        return Container(
            content=DragTarget(
                group="backlog",
                content=Column([
                            Row([Text("Product Backlog", weight=FontWeight.W_500, color=colors.BLACK, size=30)], alignment=MainAxisAlignment.CENTER),
                            body,
                        ], horizontal_alignment=CrossAxisAlignment.CENTER),
                on_will_accept=lambda e: self.set_drag_target("product_backlog"),
                on_accept=lambda e: self.move_item(),
                on_leave=lambda e: self.reset_drag_target(),
            ),
            bgcolor="#BABDE2",
            border=border.all(1.5, "#000000"),
            border_radius=border_radius.all(10),
            padding=padding.all(10),
            expand=True,
            height=self.page.height - 120,
        )
    
    def build_sprint_backlog_column(self, sprint_backlog_items=None):
        if sprint_backlog_items == []:
            body = Container(
                content=Column([
                    Text("No items in the sprint backlog", color=colors.BLACK, size=20)
                ], alignment=MainAxisAlignment.CENTER),
                expand=1,
            )

        elif sprint_backlog_items:
            body = Container(
                content=Column(
                    [],
                    alignment=MainAxisAlignment.CENTER,
                    scroll=ScrollMode.AUTO,
                    on_scroll=lambda e: print("Scrolled"),
                ),
                expand=1,
            )

            for sprint_backlog_item in sprint_backlog_items:
                body.content.controls.append(
                    DraggableItemCard(
                        group="backlog",
                        item_dict=sprint_backlog_item,
                        handle_drag_start=self.set_drag_source,
                        on_drag_complete=lambda e: self.reset_drag_source(),
                    )
                )
                body.content.controls.sort(key=lambda x: x.task_name)
        
        else:
            body = LoadingCard("Retrieving Sprint Backlog Items...")

        return Container(
            content=DragTarget(
                group="backlog",
                content=Column([
                            Row([Text("Sprint Backlog", weight=FontWeight.W_500, color=colors.BLACK, size=30)], alignment=MainAxisAlignment.CENTER),
                            body,
                        ], horizontal_alignment=CrossAxisAlignment.CENTER),
                on_will_accept=lambda e: self.set_drag_target("sprint_backlog"),
                on_accept=lambda e: self.move_item(),
                on_leave=lambda e: self.reset_drag_target(),
            ),
            bgcolor="#BABDE2",
            border=border.all(1.5, "#000000"),
            border_radius=border_radius.all(10),
            padding=padding.all(10),
            expand=True,
            height=self.page.height - 120,
        )
    
    def build(self):
        print("Building Sprint backlog")

        return Container(
            content=Column([
                Row([
                    Text("Sprint Backlog", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
                    IconButton(icon=icons.CLOSE, on_click=lambda e: self.page.go("/sprintboard")),
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Container(
                    content=Row([
                        self.build_product_backlog_column(),
                        self.build_sprint_backlog_column(),
                    ])
                )
            ]),
            padding=padding.all(20),
            border_radius=border_radius.all(10),
            bgcolor="#CADEED",
            width=self.page.width - 330,
            height=self.page.height - 20,
        )
    
    def before_update(self):
        if self.page.route.startswith("/sprintbacklog/"):
            print("\033[33mSprint backlog updated\033[0m")
            sprint_id = self.page.route.split("/")[2]
            sprint_name = asyncio.run(SprintData().get_sprint_item(sprint_id))["sprint_name"]
            if self.page:
                self.controls[0].content.controls[0].controls[0].value = sprint_name

                self.controls[0].width = self.page.width - 330
                self.controls[0].height =  self.page.height - 20

                self.controls[0].content.controls[1].content.controls[0].height = self.page.height - 120
                self.controls[0].content.controls[1].content.controls[1].height = self.page.height - 120

            asyncio.run(self.populate_product_backlog())
            asyncio.run(self.populate_sprint_backlog())

    async def populate_product_backlog(self):
        all_items = await Data().get_product_backlog_items()
        product_backlog_items = []
        for item in all_items:
            try:
                if item["sprint_id"] == "":
                    product_backlog_items.append(item)
            except KeyError:
                print("Item has no sprint_id")
        product_backlog_column = self.build_product_backlog_column(product_backlog_items)
        self.controls[0].content.controls[1].content.controls[0] = product_backlog_column
        print("Product backlog populated: ", product_backlog_items)

    async def populate_sprint_backlog(self):
        all_items = await Data().get_product_backlog_items()
        print(self.page.route)
        sprint_id = self.page.route.split("/")[2]
        sprint_backlog_items = []
        for item in all_items:
            try:
                if item["sprint_id"] == sprint_id:
                    sprint_backlog_items.append(item)
            except KeyError:
                print("Item has no sprint_id")
        sprint_backlog_column = self.build_sprint_backlog_column(sprint_backlog_items)
        self.controls[0].content.controls[1].content.controls[1] = sprint_backlog_column
        print("Sprint backlog populated: ", sprint_backlog_items)

    def set_drag_source(self, drag_source):
        print("Setting drag source", drag_source)
        self.drag_source = drag_source
        
    def reset_drag_source(self):
        print("Resetting drag source")
        self.drag_source = None

    def set_drag_target(self, drag_target):
        if drag_target == "sprint_backlog" and self.page.route.startswith("/sprintbacklog/"):
            self.controls[0].content.controls[1].content.controls[1].bgcolor = colors.GREEN_200
        elif drag_target == "product_backlog" and self.page.route.startswith("/sprintbacklog/"):
            self.controls[0].content.controls[1].content.controls[0].bgcolor = colors.GREEN_200
        self.controls[0].content.controls[1].content.update()

        print("Setting drag target", drag_target)
        self.drag_target = drag_target
    
    def reset_drag_target(self):
        self.controls[0].content.controls[1].content.controls[0].bgcolor = "#BABDE2"
        self.controls[0].content.controls[1].content.controls[1].bgcolor = "#BABDE2"
        self.controls[0].content.controls[1].content.update()
        
        print("Resetting drag target")
        self.drag_target = None

    def move_item(self):
        source = self.drag_source
        target = self.drag_target
        print("Moving item" + str(source) + " to " + target)
        if target == "product_backlog":
            source["sprint_id"] = ""
            source["logs"].append("Item updated on " + datetime.utcnow().isoformat() + " - Moved to " + target)

        elif target == "sprint_backlog":
            source["sprint_id"] = self.page.route.split("/")[2]
            print("Setting Sprint ID: ", source["sprint_id"])
            source["logs"].append(
                "Item updated on " + 
                datetime.utcnow().isoformat() + 
                " - Moved to " + 
                target + " for sprint " +
                self.page.route.split("/")[2]
                )
        id = source["_id"]
        del source["_id"]

        asyncio.run(Data().update_product_backlog_item(item_id=id, updated_fields=source))

        asyncio.run(self.populate_product_backlog())
        asyncio.run(self.populate_sprint_backlog())
        self.page.update()

    def drag_will_accept(self, e: DragTargetAcceptEvent):
        print(f"Will accept dragged item: {e.data}")
        
        # Change the background of the drop target to show it can accept the drop
        e.control.content.bgcolor = colors.GREEN  
        e.control.update()

    def drag_accept(self, e: DragTargetAcceptEvent):
        print(f"Item accepted: {e.data}")

        dropped_item = e.data 

        # Access the sprint backlog column directly from the drop target control
        sprint_backlog_column = e.control.content.controls[1].content.content

        sprint_backlog_column.append(
            Container(
                content=DraggableItemCard(dropped_item), 
                alignment=alignment.center
            )
        )

        product_backlog_column = e.control.content.controls[0].content.content
        product_backlog_column.controls = [item for item in product_backlog_column.controls if item.data != dropped_item]

        e.control.update()

    def drag_leave(self, e: DragTargetAcceptEvent):
        print(f"Dragged item left target: {e.data}")
        
        # Reset the background color of the drop target
        e.control.content.bgcolor = colors.BLUE_GREY_100 
        e.control.update()
