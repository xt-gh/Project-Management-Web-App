from flet import *
import asyncio
from datetime import datetime
import time

from data.color_data import ColourData
from data.manage_data import Data
from data.manage_sprint_data import SprintData
from views.components.ItemFormInSprint import ItemFormInSprint
from views.components.ItemCard import DraggableItemCard
from views.components.LoadingCard import LoadingCard
from views.components.BurndownChartPopup import BurndownChartPopup

class SprintKanbanView(Stack):
    def __init__(self, page):
        print("Sprint kanban initialized")
        super().__init__()
        self.page = page

        self.bgcolor = "#CADEED"
        self.padding = padding.all(15)
        self.border_radius = border_radius.all(10)

        self.width = self.page.width - 330
        self.height = self.page.height - 60

        self.drag_source = None
        self.drag_target = None

    def build_not_started_column(self, not_started_items=None):
        if not_started_items == []:
            body = Container(
                content=Column([
                    Text("No items", color=colors.BLACK, size=20)
                ], alignment=MainAxisAlignment.CENTER),
                expand=1,
            )
        
        elif not_started_items:
            body = Container(
                content=Column(
                    [],
                    alignment=MainAxisAlignment.CENTER,
                    scroll=ScrollMode.AUTO,
                    on_scroll=lambda e: print("Scrolled"),
                ),
                expand=1,
            )

            for not_started_item in not_started_items:
                body.content.controls.append(
                    DraggableItemCard(
                        group="kanban",
                        item_dict=not_started_item,
                        handle_drag_start=self.set_drag_source,
                        on_drag_complete=lambda e: self.reset_drag_source(),
                        handle_detailed_view=self.handle_detailed_view,
                    )
                )
                body.content.controls.sort(key=lambda x: x.task_name)
    
        else:
            body = LoadingCard()

        return Container(
            content=DragTarget(
                group="kanban",
                content=Column([
                            Row([Text("Not Started", weight=FontWeight.W_500, color=colors.BLACK, size=30)], alignment=MainAxisAlignment.CENTER),
                            body,
                        ], horizontal_alignment=CrossAxisAlignment.CENTER),
                on_will_accept=lambda e: self.set_drag_target("not_started"),
                on_accept=lambda e: self.move_item(),
                on_leave=lambda e: self.reset_drag_target(),
            ),
            bgcolor="#BABDE2",
            border=border.all(1.5, "#000000"),
            border_radius=border_radius.all(10),
            padding=padding.all(10),
            expand=True,
        )
    
    def build_in_progress_column(self, in_progress_items=None):
        if in_progress_items == []:
            body = Container(
                content=Column([
                    Text("No items", color=colors.BLACK, size=20)
                ], alignment=MainAxisAlignment.CENTER),
                expand=1,
            )
        
        elif in_progress_items:
            body = Container(
                content=Column(
                    [],
                    alignment=MainAxisAlignment.CENTER,
                    scroll=ScrollMode.AUTO,
                    on_scroll=lambda e: print("Scrolled"),
                ),
                expand=1,
            )

            for in_progress_item in in_progress_items:
                body.content.controls.append(
                    DraggableItemCard(
                        group="kanban",
                        item_dict=in_progress_item,
                        handle_drag_start=self.set_drag_source,
                        on_drag_complete=lambda e: self.reset_drag_source(),
                        handle_detailed_view=self.handle_detailed_view,
                    )
                )
                body.content.controls.sort(key=lambda x: x.task_name)
    
        else:
            body = LoadingCard()

        return Container(
            content=DragTarget(
                group="kanban",
                content=Column([
                            Row([Text("In Progress", weight=FontWeight.W_500, color=colors.BLACK, size=30)], alignment=MainAxisAlignment.CENTER),
                            body,
                        ], horizontal_alignment=CrossAxisAlignment.CENTER),
                on_will_accept=lambda e: self.set_drag_target("in_progress"),
                on_accept=lambda e: self.move_item(),
                on_leave=lambda e: self.reset_drag_target(),
            ),
            bgcolor="#E6DEB3",
            border=border.all(1.5, "#000000"),
            border_radius=border_radius.all(10),
            padding=padding.all(10),
            expand=True,
        )
    
    def build_completed_column(self, completed_items=None):
        if completed_items == []:
            body = Container(
                content=Column([
                    Text("No items", color=colors.BLACK, size=20)
                ], alignment=MainAxisAlignment.CENTER),
                expand=1,
            )
        
        elif completed_items:
            body = Container(
                content=Column(
                    [],
                    alignment=MainAxisAlignment.CENTER,
                    scroll=ScrollMode.AUTO,
                    on_scroll=lambda e: print("Scrolled"),
                ),
                expand=1,
            )

            for completed_item in completed_items:
                body.content.controls.append(
                    DraggableItemCard(
                        group="kanban",
                        item_dict=completed_item,
                        handle_drag_start=self.set_drag_source,
                        on_drag_complete=lambda e: self.reset_drag_source(),
                        handle_detailed_view=self.handle_detailed_view,
                    )
                )
                body.content.controls.sort(key=lambda x: x.task_name)
    
        else:
            body = LoadingCard()

        return Container(
            content=DragTarget(
                group="kanban",
                content=Column([
                            Row([Text("Completed", weight=FontWeight.W_500, color=colors.BLACK, size=30)], alignment=MainAxisAlignment.CENTER),
                            body,
                        ], horizontal_alignment=CrossAxisAlignment.CENTER),
                on_will_accept=lambda e: self.set_drag_target("completed"),
                on_accept=lambda e: self.move_item(),
                on_leave=lambda e: self.reset_drag_target(),
            ),
            bgcolor="#AED0AE",
            border=border.all(1.5, "#000000"),
            border_radius=border_radius.all(10),
            padding=padding.all(10),
            expand=True,
        )

    def build(self):
        print("Building Sprint kanban board")

        return Stack(
            controls=[
                Container(
                    content=Column([
                        Row([
                            Text("Sprint Kanban", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
                            Row([
                                ElevatedButton("Burndown Chart", icon=icons.SSID_CHART, on_click=lambda e: self.open_burndown_chart()),
                                IconButton(icon=icons.CLOSE, on_click=lambda e: self.page.go("/sprintboard")),
                            ])
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        Container(
                            content=Row([
                                self.build_not_started_column(),
                                self.build_in_progress_column(),
                                self.build_completed_column(),
                            ], expand=True),
                            expand=True,
                        )
                    ], expand=True),
                    padding=padding.all(20),
                    border_radius=border_radius.all(10),
                    bgcolor="#CADEED",
                    width=self.page.width - 330,
                    height=self.page.height - 60,
                )
            ],
            width=self.page.width - 330,
            height=self.page.height - 60,
        )
    
    
    def before_update(self):
        if self.page.route.startswith("/sprintkanban/"):
            print("\033[33mSprint kanban board updated\033[0m")
            sprint_id = self.page.route.split("/")[2]
            sprint_name = asyncio.run(SprintData().get_sprint_item(sprint_id))["sprint_name"]
            print("Sprint name:", sprint_name)

            if self.page:
                self.controls[0].controls[0].content.controls[0].controls[0].value = sprint_name

                self.controls[0].controls[0].width = self.page.width - 330
                self.controls[0].controls[0].height =  self.page.height - 60

            asyncio.run(self.populate_board())
            asyncio.run(self.set_item_list())

    async def set_item_list(self):
        sprint_id = self.page.route.split("/")[2]
        self.item_list = await Data().get_tasks_from_sprint_id(sprint_id)
    
    async def populate_board(self):
        print("Populating sprint kanban board")
        
        sprint_id = self.page.route.split("/")[2]
        sprint_items = await Data().get_tasks_from_sprint_id(sprint_id)
        not_started_items = []
        in_progress_items = []
        completed_items = []

        for sprint_item in sprint_items:
            if sprint_item["status"] == "Not Started":
                not_started_items.append(sprint_item)
            elif sprint_item["status"] == "In Progress":
                in_progress_items.append(sprint_item)
            elif sprint_item["status"] == "Completed":
                completed_items.append(sprint_item)

        print("Not started items:", not_started_items)
        print("In progress items:", in_progress_items)
        print("Completed items:", completed_items)
        
        self.controls[0].controls[0].content.controls[1].content.controls = [
            self.build_not_started_column(not_started_items),
            self.build_in_progress_column(in_progress_items),
            self.build_completed_column(completed_items),
        ]
        print("Sprint kanban board populated")

    def set_drag_source(self, drag_source):
        print("Setting drag source")
        self.drag_source = drag_source

    def reset_drag_source(self):
        print("Resetting drag source")
        self.drag_source = None

    def set_drag_target(self, drag_target):
        if drag_target == "not_started":
            self.controls[0].controls[0].content.controls[1].content.controls[0].bgcolor = colors.BLUE_300
        elif drag_target == "in_progress":
            self.controls[0].controls[0].content.controls[1].content.controls[1].bgcolor = colors.ORANGE_200
        elif drag_target == "completed":
            self.controls[0].controls[0].content.controls[1].content.controls[2].bgcolor = colors.GREEN_300
        self.controls[0].controls[0].content.controls[1].content.update()

        print("Setting drag target")
        self.drag_target = drag_target

    def reset_drag_target(self):
        self.controls[0].controls[0].content.controls[1].content.controls[0].bgcolor = "#BABDE2"
        self.controls[0].controls[0].content.controls[1].content.controls[1].bgcolor = "#E6DEB3"
        self.controls[0].controls[0].content.controls[1].content.controls[2].bgcolor = "#AED0AE"
        self.controls[0].controls[0].content.controls[1].content.update()

        print("Resetting drag target")
        self.drag_target = None

    def move_item(self):
        source = self.drag_source
        target = self.drag_target
        print("Moving item")
        
        if target == "not_started":
            source["status"] = "Not Started"
            source["date_completed"] = ""
            source["logs"].append(
                {
                    "user": self.page.current_user_info["username"],
                    "date": datetime.now().strftime("%d-%m-%Y"),
                    "time": datetime.now().strftime("%I:%M %p"),
                    "action": "Moved task to " + target + " column"
                }
            )

        elif target == "in_progress":
            source["status"] = "In Progress"
            source["date_completed"] = ""
            source["logs"].append(
                {
                    "user": self.page.current_user_info["username"],
                    "date": datetime.now().strftime("%d-%m-%Y"),
                    "time": datetime.now().strftime("%I:%M %p"),
                    "action": "Moved task to " + target + " column"
                }
            )
                    
        elif target == "completed":
            source["status"] = "Completed"
            source["date_completed"] = datetime.now().strftime("%d-%m-%Y")
            source["logs"].append(
                {
                    "user": self.page.current_user_info["username"],
                    "date": datetime.now().strftime("%d-%m-%Y"),
                    "time": datetime.now().strftime("%I:%M %p"),
                    "action": "Moved task to " + target + " column"
                }
            )

        id = source["_id"]
        del source["_id"]

        response = asyncio.run(Data().update_product_backlog_item(item_id=id, updated_fields=source))

        print(response)

        asyncio.run(self.populate_board())
        asyncio.run(self.set_item_list())
        completed = asyncio.run(self.check_completion_status())
        if completed:
            img = Image(
                # src="./assets/confettipop2.gif",
                src="https://cdn.discordapp.com/attachments/740544796736749643/1295625041425334302/confettipop2.gif?ex=670f5459&is=670e02d9&hm=50d2032e7610dca014c04b0a6f8881f4af381fc8f59fbf62fdd077d47924a227&",
                width=self.page.width - 330,
                height=self.page.height - 20,
                fit=ImageFit.COVER,
            )
            self.controls.append(img)
            
        self.page.update()
        
        if completed:
            print("Starting countdown")
            time.sleep(5)
            self.controls.pop()
            self.page.update()

    def handle_detailed_view(self, id):
        print("Detailed view clicked")
        for item in self.item_list:
            if item["_id"] == id:
                self.detailed_view = ItemFormInSprint(self.page, self.close_detailed_view, mode="view", item_dict=item)
                self.page.open(self.detailed_view)
                break
    
    def close_detailed_view(self):
        print("Closing detailed view")
        self.page.close(self.detailed_view)
        asyncio.run(self.populate_board())
        self.page.update()
    
    def open_burndown_chart(self):
        sprint_id = self.page.route.split("/")[2]
        self.burndown_popup = BurndownChartPopup(
            sprint_id=sprint_id,
            page=self.page,
            handle_close=lambda e: self.close_burndown_chart()
        )

        print(self.burndown_popup)
        self.page.open(self.burndown_popup)

    def close_burndown_chart(self):
        self.page.close(self.burndown_popup)
        self.page.update()

    def change_bg_colour(self, selected_color):
        """Change the background color of the product backlog."""
        self.bgcolor = selected_color
        self.controls[0].controls[0].bgcolor = self.bgcolor  # Update the container's background
        self.page.update()
        asyncio.run(ColourData().save_background_color("Sprint KanBan View", self.bgcolor))

    def did_mount(self):
        print("\033[33mSprint backlog mounted\033[0m")
        asyncio.run(self.load_initial_background_color())
        
    async def load_initial_background_color(self):
        color_item = await ColourData().get_color_items()  # Get color items
        for item in color_item:
            if item['component'] == "Sprint KanBan View":
                self.bgcolor = item['background_color']
                self.controls[0].controls[0].bgcolor = self.bgcolor
                break

    async def check_completion_status(self):
        sprint_id = self.page.route.split("/")[2]
        sprint_items = await Data().get_tasks_from_sprint_id(sprint_id)
        
        completed = True
        for sprint_item in sprint_items:
            if sprint_item["status"] != "Completed":
                completed = False
                break
        return completed