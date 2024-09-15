from flet import *
from .components.ItemCard import ItemCard
from .components.ItemForm import ItemForm
from .components.SprintForm import SprintForm  # Import the SprintForm component
from .components.SortPopupButton import SortPopupButton
from .components.FilterPopupButton import FilterPopupButton
from data.manage_data import Data
from data.filter_data import DataFilter 
from data.task_filter import TaskFilter
from data.task_sorter import TaskSorter
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

        self.board = GridView(
            expand=1,
            max_extent=300,
            child_aspect_ratio=1.40,
            spacing=10,
            run_spacing=10,
            padding=padding.all(5),
        )

        self.loading_screen = Container(
            content=Column([
                    ProgressRing(width=30, height=30, stroke_width=5),
                    Text("Retrieving from database...", color=colors.BLACK, size=20)
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER),
            expand=1,
        )

        self.body = self.loading_screen

        return Container(
            content=Column([
                        Row([
                            Text("Sprintboard", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
                            Row([
                                ElevatedButton("Add Sprint", icon="add", on_click=self.handle_add_sprint),
                            ], alignment=MainAxisAlignment.END),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        Container(
                            content=self.body,
                            alignment=alignment.center,
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
                self.width = self.page.width - 330
                self.height =  self.page.height - 20
        except Exception as e:
            print(e)

    async def update_board(self):
        await self.populate_board(refetch=True)
        self.update_active_view()

    def did_mount(self):
        print("\033[33mSprint board mounted\033[0m")
        asyncio.run(self.populate_board(refetch=True))
        self.controls[0].content.controls[1].content = self.board
        self.update_active_view()

    async def populate_board(self, refetch=False):
        self.board.controls.clear()
        print("Populating board")
        if refetch:
            self.item_list = await (Data().get_product_backlog_items())
            print("Fetching product backlog items")
            
        items = TaskSorter().sort_tasks(self.item_list, self.sort_label)
        items = TaskFilter().filter_tasks(items, self.filter_tag)
        for item in items:
            self.board.controls.append(
                Container(
                    content=ItemCard(item_dict=item, handle_detailed_view=self.handle_detailed_view),
                    alignment=alignment.center,
                )
            )
        print("Board populated")

    def handle_add_sprint(self, e):
        print("Add Sprint clicked")
        self.sprint_form = SprintForm(self.page, self.close_sprint_form)
        print("Opening sprint form")
        self.page.open(self.sprint_form)

    def handle_detailed_view(self, id):
        print("Detailed view clicked")
        for item in self.item_list:
            if item["_id"] == id:
                self.detailed_view = ItemForm(self.page, self.close_detailed_view, mode="view", item_dict=item)
                self.page.open(self.detailed_view)
                break

    def close_sprint_form(self):
        print("Closing sprint form")
        self.page.close(self.sprint_form)
        self.update_board()

    def close_detailed_view(self):
        print("Closing detailed view")
        self.page.close(self.detailed_view)
        self.update_board()

# from flet import *
# from .components.ItemCard import ItemCard
# from .components.ItemForm import ItemForm
# from .components.SprintForm import SprintForm
# from .components.SortPopupButton import SortPopupButton
# from .components.FilterPopupButton import FilterPopupButton
# from data.manage_data import Data
# from data.filter_data import DataFilter 
# from data.task_filter import TaskFilter
# from data.task_sorter import TaskSorter
# import asyncio



# class SprintBoard(Column):
#     def __init__(self, page, update_active_view):
#         super().__init__()
#         print("Sprint board initialized")
#         self.page = page
#         self.update_active_view = update_active_view
#         self.sprint_list = []
#         self.bgcolor = "#CADEED"
#         self.padding = padding.all(15)
#         self.border_radius = border_radius.all(10)




#         # print("Sprint board initialized")
#         # super().__init__()
#         # self.sprint_list = []
#         # # self.data = data
#         # self.page = page
#         # self.update_active_view = update_active_view


#         # self.bgcolor = "#CADEED"
#         # self.padding = padding.all(15)
#         # self.border_radius = border_radius.all(10)

#         # self.content = Text(self.data, color="black", size=32)

#     # def handle_click(self, e):
#     #     # Logic that runs when the SprintBoard is clicked
#     #     print("SprintBoard clicked!")
#     #     self.page.snack_bar = SnackBar(Text("Sprint Board Clicked!"), open=True)
#     #     self.page.update()

#     def build(self):
#         print("Building Sprintboard")

#         self.board = GridView(
#             expand=1,
#             max_extent=300,
#             child_aspect_ratio=1.40,
#             spacing=10,
#             run_spacing=10,
#             padding=padding.all(5),
#         )

#         self.loading_screen = Container(
#             content=Column([
#                     ProgressRing(width=30, height=30, stroke_width=5),
#                     Text("Retriving from database...", color=colors.BLACK, size=20)
#                 ],
#                 alignment=MainAxisAlignment.CENTER,
#                 horizontal_alignment=CrossAxisAlignment.CENTER),
#             expand=1,
#         )
    
#         self.body = self.loading_screen

#         return Container(
#             content=Column([
#                         Row([
#                             Text("Sprintboard", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
#                             Row([
#                                 ElevatedButton("Add item", icon="add", on_click=self.handle_add_sprint),
#                             ], alignment=MainAxisAlignment.END),
#                         ], alignment=MainAxisAlignment.SPACE_BETWEEN),
#                         Container(
#                             content=self.body,
#                             alignment=alignment.center,
#                             expand=1,
#                         )
#                     ]),
#             padding=padding.all(20),
#             border_radius=border_radius.all(10),
#             bgcolor="#CADEED",
#             width=self.page.width - 330,
#             height=self.page.height - 20,
#         )
    

#     def before_update(self):
#         print("\033[33mSprint board updated\033[0m")
#         try: 
#             if self.page:
#                 self.width = self.page.width - 330
#                 self.height =  self.page.height - 20
#         except Exception as e:
#             print(e)

#     async def update_board(self):
#         await self.populate_board(refetch=True)
#         self.update_active_view()

#     def did_mount(self):
#         print("\033[33mProduct backlog mounted\033[0m")
#         asyncio.run(self.populate_board(refetch=True))
#         self.controls[0].content.controls[1].content = self.board
#         self.update_active_view()

    
#     async def populate_board(self, refetch=False):
#         self.board.controls.clear()
#         print("Populating board")
#         if refetch:
#             self.item_list = await (Data().get_product_backlog_items())
#             print("Fetching product backlog items")
            
#         items = TaskSorter().sort_tasks(self.item_list, self.sort_label)
#         items = TaskFilter().filter_tasks(items, self.filter_tag)
#         for item in items:
#             self.board.controls.append(
#                 Container(
#                     content=ItemCard(item_dict=item, handle_detailed_view=self.handle_detailed_view),
#                     alignment=alignment.center,
#                 )
#             )
#         print("Board populated")

#     def handle_add_sprint(self, e):
#         print("Add item clicked")
#         self.item_form = ItemForm(self.page, self.close_add_sprint_form)
#         print("Opening form")
#         self.page.open(self.item_form)

#     def handle_detailed_view(self, id):
#         print("Detailed view clicked")
#         for item in self.item_list:
#             if item["_id"] == id:
#                 self.detailed_view = ItemForm(self.page, self.close_detailed_view, mode="view", item_dict=item)
#                 self.page.open(self.detailed_view)
#                 break


#     def close_add_sprint_form(self):
#         print("Closing form")
#         self.page.close(self.item_form)
#         self.update_board()

#     def close_detailed_view(self):
#         print("Closing detailed view")
#         self.page.close(self.detailed_view)
#         self.update_board()


#     # def close_add_sprint_form(self):
#     #     print("Closing form")
#     #     self.page.close(self.item_form)
#     #     asyncio.run(self.populate_board(refetch=True))
#     #     self.update_active_view()

#     # def close_detailed_view(self):
#     #     print("Closing detailed view")
#     #     self.page.close(self.detailed_view)
#     #     asyncio.run(self.populate_board(refetch=True))
#     #     self.update_active_view()

    


