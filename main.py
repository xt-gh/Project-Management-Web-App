import flet

from flet import *
from data.manage_data import Data
from views.SideBar import SideBar
from views.ProductBacklog import ProductBacklog
from views.Sprint import Sprint
from views.SprintBoard import SprintBoard

source_data = Data()

class App(Row):
    def __init__(self, page):
        super().__init__(page)
        self.data = source_data.get_board_items()
        self.page = page
        self.sidebar = SideBar(self.data, page)
        self.active_view = ProductBacklog(self.data, self.page,self.update_active_view)

        self.routes = {
            "/productbacklog": ProductBacklog(self.data, self.page,self.update_active_view),
            "/sprintboard": SprintBoard(),
            "/sprint": Sprint(),
        }

        self.controls=[
            self.sidebar,
            self.active_view,
            # ElevatedButton("Add Board", color="black", on_click=lambda e: self.update_active_view()),
            # Text(self.data, color="black", size=24),
        ]
        self.vertical_alignment = CrossAxisAlignment.START

    def route_change(self, e: RouteChangeEvent):
        self.active_view = self.routes[e.route]
        self.controls[1] = self.active_view
        # self.controls[3] = Text(self.data, color="black", size=24)
        self.page.update()
        print(e.route)
        print("Current route:", self.page.route)

    def update_active_view(self):
        # self.controls[3] = Text(self.data, color="black", size=24)
        self.page.update()


def main(page):

    page.title = "Project Management App"
    page.padding = 10
    page.bgcolor = "#DBEBE2"

    app = App(page)
    page.on_route_change = app.route_change

    page.add(app)

flet.app(target=main, assets_dir="./assets")