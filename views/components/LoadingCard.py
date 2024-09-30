from flet import *

class LoadingCard(Container):
    def __init__(self, message="Loading..."):
        super().__init__()
        self.content = Column([
                ProgressRing(width=30, height=30, stroke_width=5),
                Text(message, color=colors.BLACK, size=20)
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
            )
        self.expand = 1