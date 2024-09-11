from flet import *

class SprintBoard(Container):
    def __init__(self, page, data="This is the Sprint Board"):
        print("Sprint board initialized")
        super().__init__()
        self.data = data
        self.page = page

        self.bgcolor = "#CADEED"
        self.padding = padding.all(15)
        self.border_radius = border_radius.all(10)

        self.content = Text(self.data, color="black", size=32)
    
    def before_update(self):
        print("\033[33mSprint board updated\033[0m")
        try: 
            if self.page:
                self.width = self.page.width - 330
                self.height =  self.page.height - 20
        except Exception as e:
            print(e)