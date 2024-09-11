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
        self.routes = {
            "/productbacklog": ProductBacklog(self.page, self.update_active_view),
            "/sprintboard": SprintBoard(self.page),
            "/collaborators": Collaborators(self.page),
        }
        self.active_view = self.routes["/productbacklog"]

        self.controls=[self.sidebar, self.active_view]
        self.vertical_alignment = CrossAxisAlignment.START

        self.page.on_resized = lambda e: (print("Window resized"), self.update_active_view())
        asyncio.run(Data().ping())

    def route_change(self, e: RouteChangeEvent):
        self.controls[1] = self.routes[e.route]
        self.page.update()
        print("Current route:", self.page.route)

    def update_active_view(self):
        self.controls[0].update()
        self.controls[1].update()

def main(page):
    page.title = "Project Management App"
    page.padding = 10
    page.bgcolor = "#DBEBE2"
    page.theme_mode = ThemeMode.LIGHT

    app = App(page)

    page.go("/productbacklog")
    page.on_route_change = app.route_change
    page.add(app)

flet.app(target=main, assets_dir="./assets")