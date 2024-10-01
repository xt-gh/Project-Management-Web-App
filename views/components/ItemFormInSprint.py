from flet import *

from .TimeLogTable import TimeLogTable
from .TaskLogTable import TaskLogTable
from .FormComponents import DropdownInput, TextFieldInput, MultipleSelectInput
from data.manage_data import Data
from datetime import datetime
import asyncio
import re

class ItemFormInSprint(AlertDialog):
    def __init__(self, page, close_form, mode="add", item_dict=None):
        print("Item form initialized")
        super().__init__()
        self.page = page
        self.close_form = close_form
        self.mode = mode # Mode can be "add" or "view" or "edit"
        self.item_dict = item_dict
        self.content_padding = 10

        self.inset_padding = 10

        self.priotity_options = ["Low", "Medium", "Important", "Urgent"]
        self.fibbonacci = [0, 0.5, 1, 2, 3, 5, 8, 13, 20, 40, 100]
        self.story_points_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.task_stage_options = ["Planning", "Development", "Testing", "Implementation"]
        self.task_status_options = ["Not Started", "In Progress", "Completed"]
        self.task_type_options = ["User Story", "Bug"]
        self.tag_options = ["Front-end", "Back-end", "API", "Database", "UI", "UX", "Testing", "Framework"]
        self.logs = []
        self.track_time = self.item_dict.get("track_time", [])
        self.time_accumulation = self.item_dict.get("time_accumulation", [0, 0])
        
        self.bgcolor = "#CADEED"
        self.clip_behavior = ClipBehavior.HARD_EDGE
        
        self.content = self.build_add_item_form() 
        self.inset_padding = 10
        self.actions_padding = 20
        
    def build_add_item_form(self):
        self.task_name = TextFieldInput(label="Task Name", is_required=True)
        self.task_description = TextFieldInput(label="Description")
        self.task_description.multiline = True
        self.task_description.min_lines = 3
        self.priority = DropdownInput(self.priotity_options, label="Priority")
        self.story_points = DropdownInput(self.story_points_range, label="Story Points")
        self.task_stage = DropdownInput(self.task_stage_options, label="Stage")
        self.task_status = DropdownInput(self.task_status_options, label="Status")
        self.task_status.disabled = True
        self.task_type = DropdownInput(self.task_type_options, label="Type")
        self.assignee = TextFieldInput(label="Assignee", expand=False)
        self.tags = MultipleSelectInput(self.tag_options)

        
        self.chart = Container(Text("Chart Placeholder"), padding=padding.all(10), bgcolor="#FFFFFF", border_radius=border_radius.all(10))

        self.actions = [
            ElevatedButton("Cancel", bgcolor=colors.RED_300, width=100, color="black", on_click=lambda e: self.close_form()),
            ElevatedButton("Save", bgcolor=colors.GREEN_300, width=100, color="black", on_click=lambda e: self.handle_submit()),
        ]

        self.header = [
            Text("Editing Item", color="black", size=24),
            IconButton(
                icon=icons.DELETE_FOREVER,
                icon_color="black",
                on_click=lambda e: (asyncio.run(Data().remove_product_backlog_item(self.item_dict["_id"])), self.close_form()),
            )
        ]

        # item = asyncio.run(self.data.get_product_backlog_item(self.item_id))
        item = self.item_dict

        self.task_name.value = item["task_name"]
        self.task_description.value = item["description"]
        self.priority.value = item["priority"]
        self.story_points.value = item["story_points"]
        self.task_stage.value = item["stage"]
        self.task_status.value = item["status"]
        self.task_type.value = item["type"]
        self.assignee.value = item["assignee"]
        
        for tag in item["tags"]:
            self.tags.handle_add_tag(tag)
        
        self.logs = item["logs"]

        # Time tracking input field and button
        self.time_input_field = TextFieldInput("Track time (e.g. 2h30m or 2.5h)")
        add_time_button = ElevatedButton(
            "Add Time Record",
            icon=icons.ACCESS_TIME,  # Clock icon
            on_click=lambda e: self.add_time_record()
        )

        # Time log section
        
        # try:
        #     time_log_display = [
        #     Text(f"Total Accumulated Time: {self.time_accumulation[0]} hours {self.time_accumulation[1]} minutes", color="black")
        #     ] + [Text(log, color="black") for log in self.track_time] if self.track_time else [Text("No time records yet", color="black")]
        # except Exception as e:
        #     print(f"Error generating time log display: {e}")
        #     time_log_display = [Text("Error displaying time records", color="red")]        
        
        return Container(
            content=Column(
                [
                    Row(self.header, alignment=MainAxisAlignment.SPACE_BETWEEN),
                    Row([self.task_name], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    Row([self.task_description], alignment=MainAxisAlignment.SPACE_BETWEEN),

                    Row([
                        Container(self.priority, padding=padding.only(0, 0, 5, 0), expand=1),
                        Container(self.story_points, padding=5, expand=1),
                        Container(self.task_stage, padding=padding.only(5, 0, 0, 0), expand=1),
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    
                    Row([
                        Container(self.task_status, padding=padding.only(0, 0, 5, 0), expand=1),
                        Container(self.task_type, padding=5, expand=1),
                        Container(self.assignee, padding=padding.only(5, 0, 0, 0), expand=1),
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    
                    Row([Text("Tags:", color="black", size=15)]),
                    Row([self.tags]),

                    self.chart,

                    Row([self.time_input_field, add_time_button], alignment=MainAxisAlignment.SPACE_BETWEEN),

                    # Row([
                    #     Container(self.track_time,TextFieldInput("Track time (eg. 2h30m or 2.5h)",padding=padding.only(0, 0, 5, 0)),expand=1),
                    #     ElevatedButton("Add time recored",icon="ACCESS_TIME", padding=padding.only(5, 0, 0, 0), expand=1),
                    # ], alignment=MainAxisAlignment.SPACE_BETWEEN),

                    
                    # ElevatedButton("Add time record", icon="add", on_click=lambda e: print("Add time record clicked")),
                    # Row([self.chart]),

                    Column([
                        Text("Logs:", color="black", size=15),
                        Row([TaskLogTable(self.logs, width=(self.page.width * 0.4 - 40))], vertical_alignment=CrossAxisAlignment.START)
                    ]),
                    Column([
                        Text(f"Total Accumulated Time: {self.time_accumulation[0]} hours {self.time_accumulation[1]} minutes", color="black", size=20),
                        Text("Track Time Records:", color="black", size=15),
                        Row([TimeLogTable(self.track_time, width=(self.page.width * 0.4 - 40))], vertical_alignment=CrossAxisAlignment.START)
                    ]),
                ],
                on_scroll=lambda e: print("Scrolled"),
                scroll=ScrollMode.AUTO,
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
            # bgcolor="grey",
            width=self.page.width * 0.4,
            height=self.page.height * 0.7,
            padding=padding.only(15, 15, 15, 15),
            border_radius=border_radius.all(10),
            expand = 1
        )
    
    def parse_time_input(self, time_input):
        # Pattern for matching hours and minutes (e.g., 2h30m, 2.5h, 30m)
        time_pattern = r'(?:(\d+(?:\.\d*)?)h)?\s*(?:(\d+)m)?'
        
        match = re.match(time_pattern, time_input.strip())
        
        if match:
            hours = match.group(1)  # Captures the hour part
            minutes = match.group(2)  # Captures the minute part
            
            # Convert hours to minutes
            total_minutes = 0
            if hours:
                total_minutes += float(hours) * 60  # Convert to minutes
            if minutes:
                total_minutes += int(minutes)  # Add minutes
            
            # Convert back to hours and minutes
            final_hours = int(total_minutes // 60)
            final_minutes = int(total_minutes % 60)
            
            return final_hours, final_minutes
        else:
            raise ValueError("Invalid time format. Please enter a valid time format like '2h30m' or '2.5h'.")
    
    def add_time_record(self):
        # Handle adding time records
        time_record = self.time_input_field.value
        print(f"Adding time record: {time_record}")
        if time_record:
            try: 
                hours, minutes = self.parse_time_input(time_record)
                
                log_entry = {
                    "user": "John Doe",
                    "date": datetime.now().strftime("%d-%m-%Y"),
                    "time": datetime.now().strftime("%I:%M %p"),
                    "time_spent": f"{hours} hours {minutes} minutes",
                }

                self.track_time.append(log_entry)
                self.time_input_field.value = ""  # Clear input after adding
                # print(log_entry)
                self.update_time_accumulation(hours,minutes)
                
                # Update the item in the database
                item = self.item_dict
                item["track_time"] = self.track_time  # Append time record to track_time
                item["time_accumulation"] = self.time_accumulation 
                
                # Update the database with the new time log
                asyncio.run(Data().update_product_backlog_item(item_id=self.item_dict["_id"], updated_fields={
                    "track_time": item["track_time"],
                    "time_accumulation": item["time_accumulation"]
                }))
                
                self.page.update()  # Refresh the page to display new record
            except ValueError as e:
                print(e)
        else:
            print("No time entered")

    def update_time_accumulation(self, hours, minutes):
        # Convert hours to minutes and accumulate
        total_new_minutes = (hours * 60) + minutes
        
        # Initialize or update time accumulation
        self.time_accumulation = self.item_dict["time_accumulation"]

        # Add the new time to the accumulated time
        self.time_accumulation[0] += total_new_minutes // 60  # Add hours
        self.time_accumulation[1] += total_new_minutes % 60  # Add remaining minutes

        # Adjust if minutes exceed 60
        if self.time_accumulation[1] >= 60:
            self.time_accumulation[0] += self.time_accumulation[1] // 60
            self.time_accumulation[1] = self.time_accumulation[1] % 60

        print(f"Total accumulated time: {self.time_accumulation[0]} hours {self.time_accumulation[1]} minutes")


    def is_valid_form(self):
        return self.task_name.value != ""
    
    def handle_submit(self):
        if self.is_valid_form():
            print("Form is valid")
            item = {
                "task_name": self.task_name.value,
                "description": self.task_description.value,
                "priority": self.priority.value,
                "story_points": self.story_points.value,
                "stage": self.task_stage.value,
                "status": self.task_status.value,
                "type": self.task_type.value,
                "assignee": self.assignee.value,
                "tags": self.tags.selected_options,
                "track_time": self.track_time,
                "time_accumulation": [],
            }

            item["logs"] = self.logs
            item["logs"].append({
                "user": "John Doe",
                "date": datetime.now().strftime("%d-%m-%Y"),
                "time": datetime.now().strftime("%I:%M %p"),
                "action": "Updated this item"
            })
            asyncio.run(Data().update_product_backlog_item(item_id=self.item_dict["_id"], updated_fields=item))
            self.close_form()
        
        else:
            print("Form is invalid")
            self.task_name.error_text = "Task name is required"
            self.page.update()
    