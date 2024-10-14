import asyncio
from datetime import datetime, timedelta
from flet import *

from data.manage_data import Data
from data.manage_sprint_data import SprintData

class BarChartPopup(AlertDialog):
    def __init__(self, page, specific_username):
        print("Bar chart pop up")
        super().__init__()
        self.page = page
        self.specific_username = specific_username

        self.title = Text(self.specific_username, size=24, weight=FontWeight.BOLD)
        self.actions = [
            ElevatedButton(content=Text("Close", color="black"), on_click=self.close_popup, bgcolor=colors.RED_100)
        ]
        self.actions_alignment = MainAxisAlignment.END
        self.tasks = asyncio.run(Data().get_tasks_with_username(specific_username))
        all_sprints = asyncio.run(SprintData().get_sprint_items())


        today_date_object = datetime.now().date()

        for sprint in all_sprints:
            start_date_object = datetime.strptime(sprint["start_date"], '%d-%m-%Y').date()
            end_date_object = datetime.strptime(sprint["end_date"], '%d-%m-%Y').date()
            if start_date_object <= today_date_object and today_date_object <= end_date_object:
                self.current_sprint_in_progress = sprint
                break

        print(self.current_sprint_in_progress)
        self.date_range = self.get_date_range()
        self.content = self.build_popup_content()

        print(self.get_barchart_data())

    def did_mount(self):
        print("Mounted bar chart pop-up")

    def before_update(self):
        print("Before update of bar chart pop-up")
    
    def date_to_value(self, date):
        return self.date_range.index(date.strftime('%d-%m-%Y')) + 1
    
    def get_date_range(self):
        today_date = datetime.now().date()
        date_range = []
        sprint_start_date = datetime.strptime(self.current_sprint_in_progress["start_date"], "%d-%m-%Y").date()
        diff = today_date - sprint_start_date
        for day in range(diff.days + 1):
            date_range.append((sprint_start_date + timedelta(days=day)).strftime('%d-%m-%Y'))
        return date_range
    
    def get_left_axis(self):
        return ChartAxis(
            title=Text("Total hours of contribution in current sprint`", size=25, weight=FontWeight.BOLD), 
            title_size=40,
            labels_size=40, 
        )

    def get_bottom_axis(self):
        range_of_dates = self.get_date_range()

        return ChartAxis(
            title=Text("Date", size=32, weight=FontWeight.BOLD),
            title_size=50,
            labels=[
                ChartAxisLabel(
                    value=i+1,
                    label=Container(
                        content=Text(f"({str(range_of_dates[i])})", size=12),
                        padding=padding.all(10),
                        alignment=alignment.center,
                    )
                )
                for i in range(len(range_of_dates))
            ],
            labels_size=40
        )

    def get_barchart_data(self):
        bar_width = 40
        return [
            BarChartGroup(
                x=item[0],
                bar_rods=[
                    BarChartRod(
                        from_y=0,
                        to_y=item[1],
                        width = bar_width,
                        color=colors.BLUE,
                        tooltip=item[1],
                        border_radius=0,
                    )
                ]
            )
            for item in self.aggregate_hours_accumulated()
        ]

    def aggregate_hours_accumulated(self):
        date_range = self.get_date_range()
        hours_to_date = {
            self.date_to_value(datetime.strptime(date, "%d-%m-%Y")): 0
            for date in date_range
        }

        for task in self.tasks:
            tracked_time = task["track_time"]
            for log in tracked_time:
                print(log)
                if log["user"] == self.specific_username:
                    log_date = datetime.strptime(log["date"], "%d-%m-%Y") 
                    print(date_range)
                    if log["date"] in date_range:
                        hours_to_date[self.date_to_value(log_date)] += self.parse_time_to_hours(log["time_spent"])

        print(hours_to_date.items())
        return hours_to_date.items()
    
    def parse_time_to_hours(self, time_string):
        hours = int(time_string.split(" ")[0])
        minutes = int(time_string.split(" ")[2])
        hours += minutes / 60
        return hours
        

    def build_popup_content(self):
        chart = BarChart(
            bar_groups=self.get_barchart_data(),
            border=border.all(1, colors.GREY_400),
            left_axis=self.get_left_axis(),
            bottom_axis=self.get_bottom_axis(),
            horizontal_grid_lines=ChartGridLines(
                color=colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=colors.with_opacity(0.5, colors.GREY_300),
            max_y=24,
            interactive=True,
            expand=True,
        )

        return Column(
            [
                chart,
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=20,
            width=self.page.width * 0.5,
            height=self.page.height * 0.5,
        )

    def close_popup(self, e):
        print("Close bar chart pop-up")
        self.open = False
        self.page.update()
