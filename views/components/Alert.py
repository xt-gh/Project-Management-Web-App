from flet import *

class Alert(AlertDialog):
    def __init__(self, alert_text, handle_close):
        super().__init__()
        self.modal=True
        self.title=Text("Alert", color="red", size=30)
        self.content=Text(alert_text, color="black", size=20)
        self.actions=[
            TextButton("OK", on_click=lambda e: handle_close()),
        ]

        self.actions_alignment=MainAxisAlignment.END
        self.on_dismiss=lambda e: handle_close()