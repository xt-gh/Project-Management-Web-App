from flet import *
from data.color_data import ColourData
import asyncio

class Collaborators(Container):
    def __init__(self, page, data="Here are collaborators"):
        print("Collaborators initialized")
        super().__init__()
        self.data = data
        self.page = page

        self.bgcolor = "#CADEED"
        self.padding = padding.all(15)
        self.border_radius = border_radius.all(10)

        self.content = Text("Here are collaborators", color="black", size=32)
    
    def before_update(self):
        print("\033[33mCollaborators board updated\033[0m")
        if self.page:
            self.width = self.page.width - 330
            self.height =  self.page.height - 20

    async def load_initial_background_color(self):
        color_item = await ColourData().get_color_items()  # Get color items
        for item in color_item:
            if item['component'] == "Collaborators":
                self.bg_color = item['background_color']
                self.bgcolor = self.bg_color
                break
        
    def did_mount(self):
        asyncio.run(self.load_initial_background_color())

    def change_bg_colour(self, selected_color):
        """Change the background color of the product backlog."""
        self.bgcolor = selected_color
        self.bgcolor = self.bgcolor  # Update the container's background
        self.page.update()
        asyncio.run(ColourData().save_background_color("Collaborators", self.bgcolor))