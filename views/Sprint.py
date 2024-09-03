from flet import *

class Sprint(Column):
    def __init__(self, data="This is a sprint"):
        super().__init__()
        self.data = data

    def build(self):
        return Container(
            content=Text("This is a sprint", color="black", size=32),
            bgcolor="#CADEED",
            width=self.page.width * 0.7,
            height=self.page.height * 0.9,
            padding=padding.all(15),
            border_radius=border_radius.all(10),
        )