import time
import flet
from flet import *
from data.manage_data import Data
from data.manage_sprint_data import SprintData
from views.SideBar import SideBar
from views.ProductBacklog import ProductBacklog
from views.Collaborators import Collaborators
from views.SprintBoard import SprintBoard
from views.SprintBacklogView import SprintBacklogView
from views.SprintKanbanView import SprintKanbanView
from views.SprintBacklogView import SprintBacklogView
from views.SprintKanbanView import SprintKanbanView
from views.SprintListView import SprintListView
from views.components.ColourPopupButton import ColourPopupButton
from views.LogInPage import LoginPage
import asyncio
import threading

class App(Row):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.sidebar = SideBar(page)

        self.product_backlog = ProductBacklog(self.page, self.update_active_view)
        self.sprint_board = SprintBoard(self.page, self.update_active_view)
        self.collaborators = Collaborators(self.page, self.update_active_view)
        self.sprint_backlog_view = SprintBacklogView(self.page)
        self.sprint_kanban_view = SprintKanbanView(self.page)
        self.sprint_list_view = SprintListView(self.page)
        
        self.product_backlog.visible = True
        self.sprint_board.visible = False
        self.collaborators.visible = False
        self.sprint_backlog_view.visible = False
        self.sprint_kanban_view.visible = False
        self.sprint_list_view.visible = False

        self.change_color_button = ColourPopupButton(self.change_color_callback)

        self.controls = [
            Stack(
                controls=[
                    Column(controls=[self.sidebar]),
                    Row(
                        controls=[self.change_color_button],
                        alignment=MainAxisAlignment.END,  # Align button to the right
                        spacing=0,  # No space between button and sidebar
                    ),
                ]
            ),
            self.product_backlog,
            self.sprint_board,
            self.collaborators,
            self.sprint_backlog_view,
            self.sprint_kanban_view,
            self.sprint_list_view,
        ]

        # self.vertical_alignment = CrossAxisAlignment.START
        self.page.on_resized = self.on_page_resize

        self.product_backlog_data = []
        self.sprint_data = []

        # Set up a timer for regular polling
        self.timer_interval = 5  # Check every 10 seconds
        # self.start_timer()

    def on_page_resize(self, e):
        print("Window resized")
        # Update the width and height of the currently visible active view
        for control in self.controls:
            if hasattr(control, "visible") and control.visible:
                if hasattr(control, "controls") and len(control.controls) > 0:
                    outer = control.controls[0]
                    # If it's a Stack-based view (like SprintKanbanView), its controls[0] is a Stack
                    if isinstance(outer, Stack) and len(outer.controls) > 0:
                        outer = outer.controls[0]
                    
                    outer.width = self.page.width - 330
                    outer.height = self.page.height - 20
                    
                    # Special resizing logic for SprintKanbanView columns
                    if isinstance(control, SprintKanbanView):
                        try:
                            # Update Column heights inside Kanban board
                            outer.controls[0].content.controls[1].content.controls[0].height = self.page.height - 120
                            outer.controls[0].content.controls[1].content.controls[1].height = self.page.height - 120
                            outer.controls[0].content.controls[1].content.controls[2].height = self.page.height - 120
                        except Exception as ex:
                            print("Error resizing Kanban columns:", ex)
        self.page.update()

    def start_timer(self):
        """Start a background timer to poll for data changes every 10 seconds."""
        self.timer = threading.Timer(self.timer_interval, self.poll_data)
        self.timer.daemon = True  # Ensure the timer thread exits with the main thread
        self.timer.start()

    def poll_data(self):
        while True:
            # Fetch the latest data from the product backlog and sprint databases
            latest_product_backlog_data = asyncio.run(Data().get_product_backlog_items())
            latest_sprint_data = asyncio.run(SprintData().get_sprint_items())

            # Check if product backlog data has changed
            if latest_product_backlog_data != self.product_backlog_data:
                self.product_backlog_data = latest_product_backlog_data
                self.product_backlog.refresh_data()  # Assuming refresh_data updates the view

            # Check if sprint data has changed
            if latest_sprint_data != self.sprint_data:
                self.sprint_data = latest_sprint_data
                self.sprint_board.refresh_data()  # Assuming refresh_data updates the view

            # Sleep for the specified interval
            time.sleep(self.timer_interval)

    def route_change(self, e: RouteChangeEvent):
        route = e.route
        if route == "/productbacklog":
            self.product_backlog.visible = True
            self.sprint_board.visible = False
            self.collaborators.visible = False
            self.sprint_backlog_view.visible = False
            self.sprint_kanban_view.visible = False
            self.sprint_list_view.visible = False
        
        elif route == "/sprintboard":
            self.product_backlog.visible = False
            self.sprint_board.visible = True
            self.collaborators.visible = False
            self.sprint_backlog_view.visible = False
            self.sprint_kanban_view.visible = False
            self.sprint_list_view.visible = False
        
        elif route == "/collaborators":
            self.product_backlog.visible = False
            self.sprint_board.visible = False
            self.collaborators.visible = True
            self.sprint_backlog_view.visible = False
            self.sprint_kanban_view.visible = False
            self.sprint_list_view.visible = False

        elif route.startswith("/sprintbacklog/"):
            self.product_backlog.visible = False
            self.sprint_board.visible = False
            self.collaborators.visible = False
            self.sprint_backlog_view.visible = True
            self.sprint_kanban_view.visible = False
            self.sprint_list_view.visible = False

        elif route.startswith("/sprintkanban/"):
            self.product_backlog.visible = False
            self.sprint_board.visible = False
            self.collaborators.visible = False
            self.sprint_backlog_view.visible = False
            self.sprint_kanban_view.visible = True
            self.sprint_list_view.visible = False

        elif route.startswith("/sprintlist/"):
            self.product_backlog.visible = False
            self.sprint_board.visible = False
            self.collaborators.visible = False
            self.sprint_backlog_view.visible = False
            self.sprint_kanban_view.visible = False
            self.sprint_list_view.visible = True

        self.page.update()
        print("Current route:", self.page.route)

    def change_bg_colour(self, selected_color):
        """Change the background color of the product backlog."""
        self.bg_color = selected_color
        self.controls[0].bgcolor = self.bg_color  # Update the container's background
        self.page.update()

    def change_color_callback(self, selected_color):
        """Handle the color change when the button is clicked."""
        color_map = {
        "Default": ["#DBEBE2", "#CADEED", "#6686BD"],
        "Blue": ["#D8E3EC", "#B8E2F4", "#3271A5"],
        "Pink": ["#FFDBE0", "#FFD3DA", "#FFBDC7"],
        "Red": ["#FFCCCC", "#FFB3B3", "#FF8080"],
        "Orange": ["#FFDECC", "#FFCEB3", "#FFAD80"],
        "Yellow": ["#FFFFCC", "#FFFEB3", "#C9BB8E"],
        "Green": ["#DBE8D7", "#CFE1C9", "#B8D1AE"],
        "Purple": ["#E0DFF6", "#D1CFF1", "#C2BFED"],
        "Brown": ["#D9D1C4", "#C5B6A3", "#826F51"],
        "Grey": ["#CFCFCF", "#ADAAAB", "#777475"],
        "Eyeprotection": ["#DBE8D7", "#CCE8CF", "#6E7B6C"],
        "Colourblindness": ["#A8A8A8", "#333333", "#00BFFF"],
    }
        related_colors = ["#DBEBE2", "#CADEED", "#6686BD"]

        if selected_color in color_map:
            related_colors = color_map[selected_color]

        self.product_backlog.change_bg_colour(related_colors[1])
        self.sidebar.change_bg_colour(related_colors[0])
        self.sidebar.change_navigator_bg_colour(related_colors[2])
        self.sprint_board.change_bg_colour(related_colors[1])
        self.sprint_backlog_view.change_bg_colour(related_colors[1])
        self.sprint_kanban_view.change_bg_colour(related_colors[1])
        self.sprint_list_view.change_bg_colour(related_colors[1])
        self.collaborators.change_bg_colour(related_colors[1])

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
    page.fonts = {
        "Josefin_Sans" : "fonts/Josefin_Sans/static/JosefinSans-Regular.ttf"
    }
    page.theme = Theme(font_family="Josefin_Sans")
    # Create a login page and handle login logic
    def on_login_success():
        # Clear the page and navigate to the main app after login is successful
        page.clean()
        app = App(page)
        page.on_route_change = app.route_change
        page.go("/productbacklog")
        page.add(app)

    # Initialize login page with a callback to switch to the main app
    login_page = LoginPage(page, on_login_success)
    page.add(login_page)

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))
    # If PORT is specified (like in Render or Docker), start as a web app.
    # Otherwise, start as a standard desktop app.
    if os.getenv("PORT"):
        flet.app(target=main, assets_dir="./assets", view=flet.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
    else:
        flet.app(target=main, assets_dir="./assets")

