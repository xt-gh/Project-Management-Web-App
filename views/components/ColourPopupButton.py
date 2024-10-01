import flet
from flet import *

class ColourPopupButton(PopupMenuButton):
    def __init__(self, change_color_callback):
        super().__init__()
        self.icon = "palette"
        self.icon_color = "black"
        self.items = [
            PopupMenuItem(text="Default", on_click=lambda _: change_color_callback("Defaults")),
            PopupMenuItem(text="Blue", on_click=lambda _: change_color_callback("Blue")),
            PopupMenuItem(text="Pink", on_click=lambda _: change_color_callback("Pink")),
            PopupMenuItem(text="Red", on_click=lambda _: change_color_callback("Red")),
            PopupMenuItem(text="Orange", on_click=lambda _: change_color_callback("Orange")),
            PopupMenuItem(text="Yellow", on_click=lambda _: change_color_callback("Yellow")),
            PopupMenuItem(text="Green", on_click=lambda _: change_color_callback("Green")),
            PopupMenuItem(text="Purple", on_click=lambda _: change_color_callback("Purple")),
            PopupMenuItem(text="Brown", on_click=lambda _: change_color_callback("Brown")),
            PopupMenuItem(text="Grey", on_click=lambda _: change_color_callback("Grey")),
            PopupMenuItem(text="Eye Protection Mode", on_click=lambda _: change_color_callback("Eyeprotection")),
            PopupMenuItem(text="Colour Blindness Friendly", on_click=lambda _: change_color_callback("Colourblindness")),
            # Add more primary colors as needed
        ]
