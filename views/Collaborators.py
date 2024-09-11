from flet import *

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