import time
import flet
from flet import *
from data.manage_data import Data
from views.SideBar import SideBar
from views.ProductBacklog import ProductBacklog
from views.Collaborators import Collaborators
from views.SprintBoard import SprintBoard
import asyncio

class App(Row):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.sidebar = SideBar(page)
        # self.active_view = ProductBacklog(self.page, self.update_active_view)
        # self.routes = {
        #     "/productbacklog": lambda: ProductBacklog(self.page, self.update_active_view),
        #     "/sprintboard": lambda: SprintBoard(self.page, self.update_active_view),
        #     "/collaborators": lambda: Collaborators(self.page),
        # }
        # self.active_view = self.routes["/productbacklog"]()
        self.routes = {
            "/productbacklog": ProductBacklog(self.page, self.update_active_view),
            "/sprintboard": SprintBoard(self.page, self.update_active_view),
            "/collaborators": Collaborators(self.page),
        }
        self.active_view = self.routes["/productbacklog"]

        self.product_backlog = ProductBacklog(self.page, self.update_active_view)
        self.sprint_board = SprintBoard(self.page, self.update_active_view)
        self.collaborators = Collaborators(self.page)
        
        self.product_backlog.visible = True
        self.sprint_board.visible = False
        self.collaborators.visible = False

        # self.controls=[self.sidebar, self.active_view]
        self.controls = [self.sidebar, self.product_backlog, self.sprint_board, self.collaborators]


        self.vertical_alignment = CrossAxisAlignment.START
        self.page.on_resized = lambda e: (print("Window resized"), self.update_active_view())
        asyncio.run(Data().ping())

    def route_change(self, e: RouteChangeEvent):
        route = e.route
        if route == "/productbacklog":
            self.product_backlog.visible = True
            self.sprint_board.visible = False
            self.collaborators.visible = False
        
        elif route == "/sprintboard":
            self.product_backlog.visible = False
            self.sprint_board.visible = True
            self.collaborators.visible = False
        
        elif route == "/collaborators":
            self.product_backlog.visible = False
            self.sprint_board.visible = False
            self.collaborators.visible = True

        # self.controls[1] = self.routes[e.route]
        self.page.update()

        # self.update_active_view()
        # try:
        #     self.page.update()
        # except e:
        #     print(e)
        print("Current route:", self.page.route)

    def update_active_view(self):
        print("UPDATE ACTIVE VIEW")
        self.page.update()
        # self.controls[0].update()
        # self.controls[1].update()

def main(page):
    page.title = "Project Management App"
    page.padding = 10
    page.bgcolor = "#DBEBE2"
    page.theme_mode = ThemeMode.LIGHT

    app = App(page)

    page.on_route_change = app.route_change
    page.go("/productbacklog")
    page.add(app)

flet.app(target=main, assets_dir="./assets")