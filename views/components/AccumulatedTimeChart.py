import asyncio
from datetime import datetime, timedelta
from flet import *

from data.manage_sprint_data import SprintData

class AccumulatedTimeChart(LineChart):
    def __init__(self, track_time, sprint_id):
        super().__init__()
        print("AccumulatedTimeChart initialized")
        
        self.track_time = track_time
        # self.track_time = [
        #     {"date": "12-10-2024", "time_spent": "1 h 30 m"},
        #     {"date": "13-10-2024", "time_spent": "2 h 30 m"},
        #     {"date": "14-10-2024", "time_spent": "3 h 30 m"},
        # ]
        self.sprint_id = sprint_id
        self.date_range = self.get_date_range()

        self.border = Border(
            bottom=BorderSide(4, colors.with_opacity(0.5, colors.ON_SURFACE)),
            left=BorderSide(4, colors.with_opacity(0.5, colors.ON_SURFACE)),
            top=BorderSide(4, colors.with_opacity(0.5, colors.ON_SURFACE)),
            right=BorderSide(4, colors.with_opacity(0.5, colors.ON_SURFACE)),
        )
        self.min_y = 0
        self.min_x = 1
        
        self.horizontal_grid_lines = ChartGridLines(width=1, color=colors.with_opacity(0.5, colors.ON_SURFACE), interval=1)
        self.vertical_grid_lines = ChartGridLines(width=1, color=colors.with_opacity(0.5, colors.ON_SURFACE), interval=1)
        self.interactive = False

        self.data_series = self.get_data_series()
        self.left_axis = self.get_left_axis()
        self.bottom_axis = self.get_bottom_axis()
        print(self.bottom_axis)
        
    def date_to_value(self, date):
        return self.date_range.index(date.strftime('%d-%m-%Y')) + 1
    
    def aggregate_hours_accumulated(self):
        date_range = self.date_range
        hours_to_date = {
            self.date_to_value(datetime.strptime(date, "%d-%m-%Y")): 0
            for date in date_range
        }

        for tracked_time in self.track_time:
            log_date = datetime.strptime(tracked_time["date"], "%d-%m-%Y") 
            print(date_range)
            if tracked_time["date"] in date_range:
                hours_to_date[self.date_to_value(log_date)] += self.parse_time_to_hours(tracked_time["time_spent"])

        print(hours_to_date.items())
        return list(hours_to_date.items())
    
    def get_date_range(self):
        latest_date = self.get_latest_date()
        sprint = asyncio.run(SprintData().get_sprint_item(self.sprint_id))
        start_date = datetime.strptime(sprint["start_date"], "%d-%m-%Y").date()
        date_range = []
        diff = latest_date - start_date
        for day in range(diff.days + 1):
            date_range.append((start_date + timedelta(days=day)).strftime('%d-%m-%Y'))
        print("Date range:", date_range)
        return date_range
    
    def get_latest_date(self):
        latest_date = datetime.strptime(self.track_time[0]["date"], "%d-%m-%Y").date()
        for tracked_time in self.track_time:
            date = datetime.strptime(tracked_time["date"], "%d-%m-%Y").date()
            if date > latest_date:
                latest_date = date
        return latest_date
    
    def get_left_axis(self):
        return ChartAxis(
            title=Text("Hours contributed", size=20, weight=FontWeight.BOLD), 
            title_size=30,
            labels_size=40,
        )

    def get_bottom_axis(self):
        range_of_dates = self.date_range

        return ChartAxis(
            title=Text("Days Into Sprint", size=25, weight=FontWeight.BOLD),
            title_size=40,
            labels_interval=1,
            # labels=[
            #     ChartAxisLabel(
            #         value=i+1,
            #         label=Container(
            #             content=Column([
            #                 Text(f"Day {i+1}", size=15, color="black"),
            #                 Text(f"({range_of_dates[i]})", size=12),
            #             ], horizontal_alignment=CrossAxisAlignment.CENTER),
            #             padding=padding.all(10),
            #             alignment=alignment.center,
            #         )
            #     )
            #     for i in range(len(range_of_dates))
            # ],
            # labels_size=30,
        )
    
    def get_data_series(self):
        tracked_data = self.aggregate_hours_accumulated()
        print("Tracked data:", tracked_data)
        return [
            LineChartData(
                data_points=[
                    # tracked time is in the format [(date, hours), ...]
                    LineChartDataPoint(
                        tracked_data[i][0],
                        tracked_data[i][1],
                    )
                    for i in range(len(tracked_data))
                ],
                stroke_width=4,
                color=colors.BLUE,
                stroke_cap_round=True,
            )
        ]
    
    def parse_time_to_hours(self, time_string):
        hours = int(time_string.split(" ")[0])
        minutes = int(time_string.split(" ")[2])
        hours += minutes / 60
        return hours