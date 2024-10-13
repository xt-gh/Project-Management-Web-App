from flet import *
from data.manage_data import *
from datetime import datetime, timedelta
from data.manage_sprint_data import SprintData
from data.manage_data import Data
from data.manage_user_data import UserData
from .FormComponents import TextFieldDatePicker


class TableFormPopUp(AlertDialog):
    def __init__(self,page,close_form, mode="average time spent"):
        super().__init__()
        self.page = page
        self.close_form = close_form
        self.mode = mode
        self.modal = True
        self.bgcolor = "#CADEED"
        self.clip_behavior = ClipBehavior.HARD_EDGE
        self.log_list = {}
        self.prepared_log_list = {}
        
        self.title = Text("Average Log Time Spent Per Day")
        self.content = self.build_table_form() 
        self.actions = [
            ElevatedButton("Close",bgcolor=colors.RED_300, width=100, color="black", on_click=lambda e: self.close_form()),
            ]
        self.actions_alignment = MainAxisAlignment.END

    def did_mount(self):
        print("MOUNTED TABLE FORM")

    def before_update(self):
        print("BEFORE UPDATE OF TABLE FORM")

    def build_table_form(self):
        self.start_date = TextFieldDatePicker(page=self.page, label="Start Date", is_required=True)
        self.end_date = TextFieldDatePicker(page=self.page, label="End Date", is_required=True)

        if self.mode == "average time spent":
            self.header = [Text("Average Time Spent Per Day", color="black", size=24)]

        return Container(
            content=Column(
                [
                    Row([
                        Container(self.start_date, expand=1),
                        Container(self.end_date, expand=1),
                        ElevatedButton("Create Table", icon=icons.TABLE_CHART, on_click=lambda e: self.create_table(e)),                    
                    ]),
                    Text("Please choose a date range", color="black", size=20),
                ],
                on_scroll=lambda e: print("Scrolled"),
                scroll=ScrollMode.AUTO,
                alignment=MainAxisAlignment.START
            ),
            width=self.page.width * 0.5,
            height=self.page.height * 0.4,
            padding=padding.only(15, 15, 15, 15),
            border_radius=border_radius.all(10),
            expand=1
        )
    
    from datetime import datetime

    def are_dates_valid(self):
        if self.start_date.value == "":
            return "Start date is required"
        if self.end_date.value == "":
            return "End date is required"

        start_date_components = self.start_date.value.split("-")
        end_date_components = self.end_date.value.split("-")

        today_date_components = datetime.now().strftime('%d-%m-%Y').split("-")
        # Make sure the start date is not in the future
        if int(start_date_components[2]) > int(today_date_components[2]):
            return "Start date cannot be in the future"
        elif int(start_date_components[2]) == int(today_date_components[2]):
            if int(start_date_components[1]) > int(today_date_components[1]):
                return "Start date cannot be in the future"
            elif int(start_date_components[1]) == int(today_date_components[1]):
                if int(start_date_components[0]) > int(today_date_components[0]):
                    return "Start date cannot be in the future"

        # Make sure the start date is before or the same as the end date
        if int(start_date_components[2]) > int(end_date_components[2]):
            return "End date should be after start date"
        elif int(start_date_components[2]) == int(end_date_components[2]):
            if int(start_date_components[1]) > int(end_date_components[1]):
                return "End date should be after start date"
            elif int(start_date_components[1]) == int(end_date_components[1]):
                if int(start_date_components[0]) > int(end_date_components[0]):
                    return "End date should be after start date"

        return True
    

    def is_valid_form(self):
        is_valid = True  
        if self.start_date.value == "":
            is_valid = False
        
        if self.end_date.value == "":
            is_valid = False

        if self.are_dates_valid() is not True:
            is_valid = False

        return is_valid

    

    def create_table(self, e):
            # Check if the form is valid before creating the table
            if self.is_valid_form():
                print("Form is valid")

                # Dummy log data for users over two days
                self.log_list = self.get_log_list()

                # Calculate average time spent
                average_time_data = self.calculate_average_time_spent(
                    self.start_date.value,
                    self.end_date.value,
                    self.log_list
                )

                print("Average Time Data:", average_time_data)

                # Prepare the log list for the table
                self.prepared_log_list = {
                    user: avg for user, avg in average_time_data.items()
                }
                print(self.prepared_log_list)
                # Create the table and add it to the page
                table_form = TableForm(self.prepared_log_list)
                self.content.content.controls[1] = table_form
                self.page.update()  # Refresh the UI
            else:
                # Handle form validation errors
                if self.start_date.value == "":
                    self.start_date.content.controls[1].error_text = "Start date is required"
                if self.end_date.value == "":
                    self.end_date.content.controls[1].error_text = "End date is required"
                
                if self.are_dates_valid() is not True:
                    date_error_message = self.are_dates_valid()
                    if date_error_message.startswith("Start"):
                        self.start_date.content.controls[1].error_text = date_error_message
                    elif date_error_message.startswith("End"):
                        self.end_date.content.controls[1].error_text = date_error_message
                
                self.page.update()

    
    def calculate_average_time_spent(self, start_date_str, end_date_str, log_list):
        # Parse the start and end dates
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        end_date = datetime.strptime(end_date_str, "%d-%m-%Y")

        # Calculate the total number of days in the date range
        num_days = (end_date - start_date).days + 1

        # Dictionary to store total hours spent by each user
        total_time_spent = {}

        print(log_list)
        # Iterate through the logs for each user
        for user, days in log_list.items():
            total_time = 0  # Total time for the current user across all days

            for date, time_spent in days.items():
                # Convert time format to hours
                date = datetime.strptime(date, "%d-%m-%Y")

                if start_date <= date <= end_date:
                    total_time += time_spent

            total_time_spent[user] = total_time

        # Calculate average time spent per day for each user
        average_time_spent = {user: total / num_days for user, total in total_time_spent.items()}

        return average_time_spent
    
    async def get_user_contribution(self, user_id):
        contributions = {}
        tasks = await (Data().get_product_backlog_items())
        user = await (UserData().get_user_by_id(user_id))
        print(user)
        user_name = user.get('username')

        date_range = self.generate_date_range(self.start_date.value, self.end_date.value)
        for date in date_range:
            contributions[date] = 0.0
        
        for task in tasks:
            for entry in task.get('track_time', []):
                if entry['user'] == user_name:
                    # Convert date to a consistent format (e.g., just date without time)
                    date = entry['date']
                    hours_spent = self.parse_time_spent(entry['time_spent'])  # Assuming hours are stored as strings
                    print(hours_spent)

                    if date in contributions:
                        contributions[date]+= hours_spent
                    else:
                        contributions[date] = hours_spent

        return contributions

    def parse_time_spent(self,time_str):
            parts = time_str.split()
            hours = int(parts[0])  # Extract hours
            minutes = int(parts[2])  # Extract minutes
            total_hours = hours + minutes / 60.0  # Convert minutes to hours
            return total_hours

    # Helper function to generate a list of dates between two given dates
    def generate_date_range(self, start_date, end_date):
        start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
        end_date = datetime.strptime(end_date, "%d-%m-%Y").date()
        date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        return [date.strftime("%d-%m-%Y") for date in date_list]
    
    def get_log_list(self):
        log_list = {}
        users = asyncio.run(UserData().get_all_users())
        for user in users:
            user_id = user.get('_id')
            contributions = asyncio.run(self.get_user_contribution(user_id))
            username = user.get('username')
            log_list[username] = contributions

        return log_list

class TableForm(DataTable):
    def __init__(self, log_list, **kwargs):
        # Define columns for the DataTable
        columns = [
            DataColumn(Text("User")),
            DataColumn(Text("Average Log Time Spent Per Day"), numeric=True),
        ]

        # Initialize an empty list of rows
        rows = []

        # If the log_list is provided, construct the rows
        if log_list:
            for user, avg_time in log_list.items():
                hours = int(avg_time)
                minutes = int((avg_time - hours) * 60)
                time_string = f"{hours} hours {minutes} minutes"
            
                rows.append(
                    DataRow(
                        cells=[
                            DataCell(Text(user)),
                            DataCell(Text(time_string)),
                        ],
                    )
                )

        # Call the parent constructor with the columns and rows
        super().__init__(columns=columns, rows=rows, **kwargs)

        # Set additional properties
        self.bgcolor = "#CADEED"
        self.border = border.all(1, "#000000")
        self.border_radius = 10