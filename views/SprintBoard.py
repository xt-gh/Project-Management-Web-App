from flet import *

class SprintBoard(Column):
    def __init__(self, data="This is the Sprint Board"):
        super().__init__()
        self.data = data

    def build(self):
        return Container(
            content=Text(self.data, color="black", size=32),
            bgcolor="#CADEED",
            width=self.page.width * 0.7,
            height=self.page.height * 0.9,
            padding=padding.all(15),
            border_radius=border_radius.all(10),
       )