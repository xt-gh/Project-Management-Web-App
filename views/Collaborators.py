from flet import *
from data.color_data import ColourData
from data.manage_user_data import UserData
from views.components.LoadingCard import LoadingCard
from .components.CreateAccountForm import CreateAccountForm
from .components.AccountCard import AccountCard
from .components.TableFormPopUp import TableFormPopUp
from .components.TableFormPopUp import TableForm



import asyncio

class Collaborators(Column):
    def __init__(self, page, update_active_view):
        print("Collaborators initialized")
        super().__init__()
        # self.data = data
        self.page = page
        self.update_active_view = update_active_view
        self.account_list = []
        self.bgcolor = "#CADEED"
        self.padding = padding.all(15)
        self.border_radius = border_radius.all(10)

        # self.content = Text("Here are collaborators", color="black", size=32)

    def build(self):
        self.board = Column(
            scroll=ScrollMode.AUTO,
            on_scroll=lambda e: print("Scrolled"),
        )
        if self.page.current_user_info["account_type"] == "admin":
            return Container(
                 content=Column([
                    Row([
                        Text("Collaborators", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
                        Row([
                            ElevatedButton("Create Account", icon="account", on_click=lambda e: self.handle_add_user_account(e)),
                        ], alignment=MainAxisAlignment.END),
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    Container(
                        content=LoadingCard(),
                        alignment=alignment.top_center,
                        expand=1,
                    ),
                    Row([
                        ElevatedButton("Average log time spent", icon=icons.ACCESS_TIME, on_click=lambda e: self.handle_view_table(e)),
                    ], alignment=MainAxisAlignment.END),   
                ], expand=True),
                padding=padding.all(20),
                border_radius=border_radius.all(10),
                bgcolor="#CADEED",
                expand=True,
            )
        else:
            return Container(
            content=Column([
                Row([
                    Text("Collaborators", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
                ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                Container(
                    content=LoadingCard(),
                    alignment=alignment.top_center,
                    expand=1,
                )
            ], expand=True),
            padding=padding.all(20),
            border_radius=border_radius.all(10),
            bgcolor="#CADEED",
            expand=True,
        )
    
    def before_update(self):
        print("\033[33mCollaborators board updated\033[0m")
        if self.page.route.startswith("/collaborators"):
            asyncio.run(self.populate_board())

    async def load_initial_background_color(self):
        color_item = await ColourData().get_color_items()  # Get color items
        for item in color_item:
            if item['component'] == "Collaborators":
                self.bg_color = item['background_color']
                self.controls[0].bgcolor = self.bg_color
                break
        
    def did_mount(self):
        asyncio.run(self.load_initial_background_color())
        asyncio.run(self.populate_board(refetch=True))
        self.controls[0].content.controls[1].content = self.board
        self.page.update()

    async def populate_board(self, refetch=False):
        self.board.controls.clear()
        print("Populating user board")
        if refetch:
            self.account_list = await (UserData().get_all_users())
            print("Fetching user account items")
            
        # items = TaskSorter().sort_tasks(self.item_list, self.sort_label)
        # items = TaskFilter().filter_tasks(items, self.filter_tag)
        items = self.account_list
        for item in items:
            self.board.controls.append(
                Container(
                    content=AccountCard(self.refresh_page, page=self.page, account_dict=item, handle_detailed_view=self.handle_detailed_view),
                    alignment=alignment.center,
                    padding=padding.only(0,0,10,0),
                )
            )
        print("Board populated")

    def handle_add_user_account(self, e):
        print("Add account clicked")
        self.account_form = CreateAccountForm(self.page, self.close_add_user_form)
        print("Opening account form")
        self.page.open(self.account_form)

    def close_add_user_form(self):
        print("Closing account form")
        self.page.close(self.account_form)
        asyncio.run(self.populate_board(refetch=True))
        self.page.update()

    def handle_detailed_view(self, id):
        print("Detailed view clicked")
        for account in self.account_list:
            if account["_id"] == id:
                self.detailed_view = CreateAccountForm(self.page, self.close_detailed_view, mode="view", account_dict= account)
                self.page.open(self.detailed_view)
                break

    def close_detailed_view(self):
        print("Closing detailed view")
        self.page.close(self.detailed_view)
        asyncio.run(self.populate_board(refetch=True))
        self.page.update()

    def handle_view_table(self, e):
        print("Display table form")
        self.table_form = TableFormPopUp(self.page, self.close_table_form)
        print("Opening table form")
        self.page.open(self.table_form)

    def close_table_form(self):
        print("Closing table form")
        self.page.close(self.table_form)
        asyncio.run(self.populate_board(refetch=True))
        self.page.update()
    

    def change_bg_colour(self, selected_color):
        """Change the background color of the product backlog."""
        self.bgcolor = selected_color
        self.controls[0].bgcolor = self.bgcolor  # Update the container's background
        self.page.update()
        asyncio.run(ColourData().save_background_color("Collaborators", self.bgcolor))

    def refresh_page(self):
        print("refresh page")
        asyncio.run(self.populate_board(refetch=True))
        self.page.update()