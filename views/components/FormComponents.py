from flet import *

class DropdownInput(Dropdown):
    def __init__(self, options, expand=1, is_required=False):
        super().__init__()
        self.options_fill_horizontally = False
        self.expand = expand
        self.options = [dropdown.Option(val) for val in options]
        self.fill_color = "#95A8C7"
        self.on_blur = self.handle_blur
        self.on_change = self.handle_change
        self.is_required = is_required

    def handle_blur(self, e):
        print("on_blur fired", self.value, "is the value")
        if self.is_required:
            if self.value is None:
                self.error_text = "This field is required"
            else:
                self.error_text = None
            self.update()
        
    def handle_change(self, e):
        print("on_change fired")
        if self.is_required:
            if self.value is None:
                self.error_text = "This field is required"
            else:
                self.error_text = None
            self.update()
        

class TextFieldInput(TextField):
    def __init__(self, label="", expand=1, is_required=False):
        super().__init__()
        self.label = label
        self.expand = expand
        self.color = "black"
        self.size = 20
        self.fill_color = "white"
        self.on_blur = self.handle_blur
        self.on_change = self.handle_change
        self.is_required = is_required

    def handle_blur(self, e):
        print("on_blur fired")
        if self.is_required:
            if self.value is "":
                self.error_text = "This field is required"
            else:
                self.error_text = None
            self.update()
    
    def handle_change(self, e):
        print("on_change fired")
        if self.is_required:
            if self.value is "":
                self.error_text = "This field is required"
            else:
                self.error_text = None
            self.update()

class MultipleSelectInput(Row):
    def __init__(self, options, expand=1, is_required=False):
        super().__init__()
        self.options = options
        self.is_required = is_required
        self.selected_options = []
        self.controls = [self.build_popup_menu()]
        self.disabled = False

        self.wrap = True
        self.tight = True
        
        self.expand = expand
    
    def handle_add_tag(self, tag):
        print("Add tag clicked for item", tag)
        self.selected_options.append(tag)
        print("REMOVING TAG", tag)
        self.options.remove(tag)
        self.add_chip(tag)
        if self.options == []:
            self.controls.pop()
        else:
            self.controls[-1] = self.build_popup_menu()
    
    def add_chip(self, tag):
        chip = Chip(label=Text(tag, color="white"),
                    color="green",
                    border_side=BorderSide(color="white", width=1),
                    )
        if not self.disabled:
            chip.on_delete = lambda e: (self.handle_remove_tag(e.control.label.value), self.update())
            chip.delete_icon_color = "white"

        self.controls.insert(-1, chip)

    def handle_remove_tag(self, tag):
        print("Remove tag clicked for item", tag)
        self.selected_options.remove(tag)
        self.options.append(tag)
        self.remove_chip(tag)
        
        if len(self.options) == 1:
            self.controls.append(self.build_popup_menu())
        else:
            self.controls[-1] = self.build_popup_menu()

    def remove_chip(self, tag):
        for control in self.controls:
            if isinstance(control, Chip):
                if control.label.value == tag:
                    self.controls.remove(control)
                    break
    
    def build_popup_menu(self):
        return PopupMenuButton(
            items=[
                PopupMenuItem(text=option, on_click=lambda e: (self.handle_add_tag(e.control.text), self.update())) for option in self.options
            ],
            icon=icons.ADD,icon_color="black"
        )
    
    # @property
    # def disabled(self):
    #     return self._disabled
    
    # @disabled.setter
    # def disabled(self, value):
    #     self._disabled = value
    #     if self._disabled:
    #         self.controls.pop() # remove the popup menu

    #         for control in self.controls:
    #             if isinstance(control, Chip):
    #                 control.on_delete = None