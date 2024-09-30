from flet import *
from .components.SprintCard import SprintCard
from .components.SprintForm import SprintForm
from data.manage_data import Data
from data.manage_sprint_data import SprintData
import asyncio

class SprintBoard(Column):
    def __init__(self, page, update_active_view):
        super().__init__()
        print("Sprint board initialized")
        self.page = page
        self.update_active_view = update_active_view
        self.sprint_list = []
        self.bgcolor = "#CADEED"
        self.padding = padding.all(15)
        self.border_radius = border_radius.all(10)

    def build(self):
        print("Building Sprintboard")

        self.board = Column(
            scroll=ScrollMode.AUTO,
            on_scroll=lambda e: print("Scrolled"),
        )

        self.loading_screen = Container(
            content=Column([
                    ProgressRing(width=30, height=30, stroke_width=5),
                    Text("Retrieving Sprints From Database...", color=colors.BLACK, size=20)
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER),
        )

        self.body = self.loading_screen

        return Container(
            content=Column([
                        Row([
                            Text("Sprintboard", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
                            Row([
                                ElevatedButton("Add Sprint", icon="add", on_click=lambda e: self.handle_add_sprint(e)),
                                ElevatedButton("Add Sprint", icon="add", on_click=lambda e: self.handle_add_sprint(e)),
                            ], alignment=MainAxisAlignment.END),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        Container(
                            content=self.body,
                            alignment=alignment.top_center,
                            expand=1,
                        )
                    ]),
            padding=padding.all(20),
            border_radius=border_radius.all(10),
            bgcolor="#CADEED",
            width=self.page.width - 330,
            height=self.page.height - 20,
        )

    def before_update(self):
        print("\033[33mSprint board updated\033[0m")
        try: 
            if self.page:
                self.controls[0].width = self.page.width - 330
                self.controls[0].height =  self.page.height - 20
        except Exception as e:
            print(e)

    def did_mount(self):
        print("\033[33mSprint board mounted\033[0m")
        asyncio.run(SprintData().get_sprint_items())
        asyncio.run(self.populate_board(refetch=True))
        self.controls[0].content.controls[1].content = self.board
        self.page.update()

    async def populate_board(self, refetch=False):
        self.board.controls.clear()
        print("Populating board")
        if refetch:
            self.sprint_list = await (SprintData().get_sprint_items())
            print("Fetching product backlog items")
            
        # items = TaskSorter().sort_tasks(self.item_list, self.sort_label)
        # items = TaskFilter().filter_tasks(items, self.filter_tag)
        items = self.sprint_list
        for sprint in items:
            self.board.controls.append(
                Container(
                    content=SprintCard(page=self.page, sprint_dict=sprint, handle_detailed_view=self.handle_detailed_view),
                    alignment=alignment.center,
                    padding=padding.only(0,0,10,0),
                )
            )
        print("Board populated")
        # items = TaskSorter().sort_tasks(self.item_list, self.sort_label)
        # items = TaskFilter().filter_tasks(items, self.filter_tag)
        items = self.sprint_list
        for sprint in items:
            self.board.controls.append(
                Container(
                    content=SprintCard(page=self.page, sprint_dict=sprint, handle_detailed_view=self.handle_detailed_view),
                    alignment=alignment.center,
                    padding=padding.only(0,0,10,0),
                )
            )
        print("Board populated")

    def handle_add_sprint(self, e):
        print("Add Sprint clicked")
        self.sprint_form = SprintForm(self.page, self.close_sprint_form)
        print("Opening sprint form")
        self.page.open(self.sprint_form)

    def close_sprint_form(self):
        print("Closing sprint form")
        self.page.close(self.sprint_form)
        asyncio.run(self.populate_board(refetch=True))
        self.page.update()

    def handle_detailed_view(self, id):
        print("Detailed view clicked") 
        for sprint in self.sprint_list:
            if sprint["_id"] == id:
                self.detailed_view = SprintForm(self.page, self.close_detailed_view, mode="view", sprint_dict=sprint)
                self.page.open(self.detailed_view)
                break

    def close_detailed_view(self):
        print("Closing detailed view")
        self.page.close(self.detailed_view)
        asyncio.run(self.populate_board(refetch=True))
        self.page.update()