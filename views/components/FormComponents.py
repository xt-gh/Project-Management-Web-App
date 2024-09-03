from flet import *

class DropdownInput(Dropdown):
    def __init__(self, options, expand=False):
        super().__init__()
        self.options_fill_horizontally = False
        self.expand = expand
        self.options = [dropdown.Option(val) for val in options]
        self.fill_color = "#95A8C7"
        

class TextFieldInput(TextField):
    def __init__(self, label="", expand=1):
        super().__init__()
        self.label = label
        self.expand = expand
        self.color = "black"
        self.size = 20
        self.fill_color = "white"