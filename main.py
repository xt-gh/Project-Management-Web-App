import flet

from flet import *
from data.manage_data import Data
from views.SideBar import SideBar
from views.ProductBacklog import ProductBacklog
from views.Sprint import Sprint
from views.SprintBoard import SprintBoard


class App(Row):
    def __init__(self, page):
        super().__init__()
        self.data = Data()
        self.page = page
        self.sidebar = SideBar(self.data, page)
        self.active_view = ProductBacklog(self.page, self.update_active_view)
        self.routes = {
            "/productbacklog": ProductBacklog(self.page, self.update_active_view),
            "/sprintboard": SprintBoard(),
            "/sprint": Sprint(),
        }

        self.controls=[self.sidebar, self.active_view]
        self.vertical_alignment = CrossAxisAlignment.START

    def route_change(self, e: RouteChangeEvent):
        self.active_view = self.get_active_view(e.route)
        self.controls[-1] = self.active_view
        self.page.update()
        print("Current route:", self.page.route)

    def update_active_view(self):
        self.controls[-1] = self.get_active_view(self.page.route)
        self.page.update()

    def get_active_view(self, route):
        routes = {
            "/productbacklog": ProductBacklog(self.page, self.update_active_view),
            "/sprintboard": SprintBoard(),
            "/sprint": Sprint(),
        }
        return routes[route]

def main(page):

    page.title = "Project Management App"
    page.padding = 10
    page.bgcolor = "#DBEBE2"

    app = App(page)

    page.go("/productbacklog")
    page.on_route_change = app.route_change
    page.add(app)

flet.app(target=main, assets_dir="./assets")