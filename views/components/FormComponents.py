from datetime import datetime
from flet import *

class DropdownInput(Dropdown):
    def __init__(self, options, label="", expand=False, is_required=False):
        super().__init__()
        self.label = label
        # self.label_style = TextStyle(color="black", size=15)

        self.options_fill_horizontally = False
        self.expand = expand
        self.options = [dropdown.Option(val) for val in options]
        self.fill_color = "white"
        self.color = "black"
        self.on_blur = self.handle_blur
        self.on_change = self.handle_change
        self.is_required = is_required
        self.priority_colors = {
            "Low": colors.GREEN_300,
            "Medium": colors.YELLOW_300,
            "Important": colors.ORANGE_300,
            "Urgent": colors.RED_300,
        }

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
        if self.value in self.priority_colors.keys():
            self.fill_color = self.priority_colors[self.value]
            self.update()
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
        # self.label_style = TextStyle(color="black", size=15)
        self.border_color = "black"

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
            if self.value.strip() == "":
                self.error_text = "This field is required"
            else:
                self.error_text = None
            self.update()
    
    def handle_change(self, e):
        print("on_change fired")
        if self.is_required:
            if self.value.strip() == "":
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
        self.tag_colors = {
            "Front-end": "#FA9189",
            "Back-end": "#FCAE7C",
            "API": "#FFE699",
            "Database": "#F9FFB5",
            "UI": "#B3F5BC",
            "UX": "#D6F6FF",
            "Testing": "#E2CBF7",
            "Framework": "#D1BDFF",
        }
    
    def handle_add_tag(self, tag):
        # print("Add tag clicked for item", tag)
        self.selected_options.append(tag)
        print("REMOVING TAG", tag)
        self.options.remove(tag)
        self.add_chip(tag)
        if self.options == []:
            self.controls.pop()
        else:
            self.controls[-1] = self.build_popup_menu()
    
    def add_chip(self, tag):
        chip_color = "#DBEBE2"
        if tag in self.tag_colors.keys():
            chip_color = self.tag_colors[tag]

        chip = Chip(label=Text(tag, color="black"),
                    color=chip_color,
                    border_side=BorderSide(color="white", width=1),
                    )
        if not self.disabled:
            chip.on_delete = lambda e: (self.handle_remove_tag(e.control.label.value), self.update())
            chip.delete_icon_color = "black"

        self.controls.insert(-1, chip)

    def handle_remove_tag(self, tag):
        # print("Remove tag clicked for item", tag)
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
    
class TextFieldDatePicker(Container):
    def __init__(self, page, label="", expand=1, is_required=False):
        super().__init__()
        self.page = page
        self.is_required = is_required
        self.label = label

        self.content = Row(
            [
                IconButton(
                    icon=icons.CALENDAR_MONTH,
                    icon_size=30,
                    on_click=lambda e: self.open_date_picker(e),
                ),
                TextField(
                    label=label,
                    border_color="black",
                    expand=expand,
                    color="black",
                    fill_color="white",
                    read_only=True,
                ),
            ],
            vertical_alignment=CrossAxisAlignment.START,
        )
        
        self.value = self.content.controls[1].value
        # self.width = ""
        # self.height = "50"
        

    def open_date_picker(self, e):
        print("opening date picker")
        self.page.open(
            DatePicker(
                first_date=datetime(year=2015, month=1, day=1),
                help_text=self.label,
                on_change=lambda e: self.change_date_picker_handler(e), 
            )
        )

    def change_date_picker_handler(self, e):
        print("Date changed")
        self.content.controls[1].error_text = None
        self.content.controls[1].value = e.control.value.strftime('%d-%m-%Y')
        self.value = self.content.controls[1].value
        self.update()
    
    def set_date(self, date):
        self.content.controls[1].value = date
        self.value = date