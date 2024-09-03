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

class MultipleSelectInput(GridView):
    def __init__(self, options, is_required=False):
        super().__init__()
        self.options = options
        self.is_required = is_required
        self.selected_options = []
        self.controls = [self.build_popup_menu()]
        
        self.expand = 1
        self.runs_count = 3
        self.max_extent = 150
        self.child_aspect_ratio = 4.5
    
    def handle_add_tag(self, e):
        print("Add tag clicked for item", e.control.text)
        self.selected_options.append(e.control.text)
        self.options.remove(e.control.text)
        self.add_chip(e.control.text)
        if self.options == []:
            self.controls.pop()
        else:
            self.controls[-1] = self.build_popup_menu()
        self.update()
    
    def add_chip(self, tag):
        chip = Chip(label=Text(tag, color="black"),
                    bgcolor=colors.GREEN_200,
                    on_delete = self.handle_remove_tag,
                    delete_icon_color="black",
                    width=200
                    )
        self.controls.insert(-1, chip)

    def handle_remove_tag(self, e):
        print(vars(e.control))
        print("Remove tag clicked for item", e.control.label.value)
        self.selected_options.remove(e.control.label.value)
        self.options.append(e.control.label.value)
        self.remove_chip(e.control.label.value)
        
        if len(self.options) == 1:
            self.controls.append(self.build_popup_menu())
        else:
            self.controls[-1] = self.build_popup_menu()
        self.update()

    def remove_chip(self, tag):
        for control in self.controls:
            if isinstance(control, Chip):
                if control.label.value == tag:
                    self.controls.remove(control)
                    break
    
    def build_popup_menu(self):
        return PopupMenuButton(
            items=[
                PopupMenuItem(text=option, on_click=self.handle_add_tag) for option in self.options
            ],
            icon=icons.ADD,
        )