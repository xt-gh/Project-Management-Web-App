import asyncio
from datetime import datetime, timedelta
from flet import *
from data.manage_sprint_data import SprintData
from data.manage_data import Data

class BurndownChartPopup(AlertDialog):
    def __init__(self, sprint_id, page, handle_close):
        super().__init__()
        print("BurndownChartPopup initialized")
        self.sprint_id = sprint_id
        self.page = page
        self.handle_close = handle_close

        self.title = Text("Burndown Chart", size=40, weight=FontWeight.BOLD)
        self.actions = [
            TextButton("Close", on_click=handle_close)
        ]
        self.actions_alignment=MainAxisAlignment.END
        self.sprint_tasks = asyncio.run(Data().get_tasks_from_sprint_id(sprint_id))
        self.sprint = asyncio.run(SprintData().get_sprint_item(sprint_id))
        
        sprint_start_date, sprint_end_date = self.get_sprint_dates()
        self.date_range = self.get_date_range(sprint_start_date, sprint_end_date)
        self.content = self.build_chart()

    def did_mount(self):
        print("MOUNTED BURN DOWN CHART")

    def before_update(self):
        print("BEFORE UPDATE OF BURN DOWN CHART")

    def date_to_value(self, date):
        return self.date_range.index(date.strftime('%d-%m-%Y')) + 1

    def get_date_range(self, start_date, end_date):
        date_range = []
        diff = end_date - start_date
        for day in range(diff.days + 1):
            date_range.append((start_date + timedelta(days=day)).strftime('%d-%m-%Y'))
        return date_range
    
    def get_left_axis(self, total_story_points):
        return ChartAxis(
            title=Text("Story Points", size=32, weight=FontWeight.BOLD),
            title_size=40,
            labels=[
                ChartAxisLabel(
                    value=i+1,
                    label=Container(
                        content=Text(str(i+1), size=14, weight=FontWeight.BOLD),
                        padding=padding.all(10),
                        alignment=alignment.center,
                    )
                ) 
                for i in range(total_story_points)
            ],
            labels_size=40,
        )
    
    def get_bottom_axis(self, range_of_dates):
        return ChartAxis(
            title=Text("Day", size=32, weight=FontWeight.BOLD),
            title_size=80,
            labels=[
                ChartAxisLabel(
                    value=i+1,
                    label=Container(
                        content=Column([
                            Text(f"Day {i+1}", size=15),
                            Text(f"({str(range_of_dates[i])})", size=12),
                        ], horizontal_alignment=CrossAxisAlignment.CENTER),
                        padding=padding.all(10),
                        alignment=alignment.center,
                    )
                )
                for i in range(len(range_of_dates))
            ],
            labels_size=32,
        )
    
    def get_total_story_points(self, tasks):
        total_story_points = 0
        for task in tasks:
            total_story_points += int(task.get('story_points', 0))
        return total_story_points
    
    def get_chart_data(self):
        burndown_data, ideal_burndown_data = self.aggregate_story_points_by_date()        
        print("Date range", self.date_range)
        print("Building burndown chart")
        print("Ideal burndown data", ideal_burndown_data)
        print("Burndown data", burndown_data)

        ideal_data = LineChartData(
            data_points=[
                # ideal_burndown_data is in the format [(points, date), ...]
                LineChartDataPoint(
                    ideal_burndown_data[0][0],
                    ideal_burndown_data[0][1],
                    tooltip="Ideal burndown: " + self.date_range[ideal_burndown_data[0][0]-1],
                    tooltip_style=TextStyle(
                        color=colors.WHITE, bgcolor=colors.with_opacity(0.5, colors.RED)
                    ),
                ),
                LineChartDataPoint(
                    ideal_burndown_data[1][0],
                    ideal_burndown_data[1][1],
                    tooltip="Ideal burndown " + self.date_range[ideal_burndown_data[1][0]-1],
                    tooltip_style=TextStyle(
                        color=colors.WHITE, bgcolor=colors.with_opacity(0.5, colors.RED)
                    ),
                ),
            ],
            stroke_width=4,
            color=colors.with_opacity(0.5, colors.RED),
            stroke_cap_round=True,
        )

        actual_data = LineChartData(
            data_points=[
                # burndown_data is in the format [(points, date), ...]
                LineChartDataPoint(
                    burndown_data[i][0],
                    burndown_data[i][1],
                    tooltip="Actual burndown: " + self.date_range[burndown_data[i][0]-1],
                    tooltip_style=TextStyle(
                        color=colors.WHITE, bgcolor=colors.with_opacity(0.5, colors.RED)
                    ),
                )
                for i in range(len(burndown_data))
            ],
            stroke_width=4,
            color=colors.with_opacity(0.5, colors.LIGHT_BLUE),
            stroke_cap_round=True,
        )

        return [ideal_data, actual_data]


    def build_chart(self):
        chart = LineChart(
            data_series=self.get_chart_data(),
            border=Border(
                bottom=BorderSide(4, colors.with_opacity(0.5, colors.ON_SURFACE)),
                left=BorderSide(4, colors.with_opacity(0.5, colors.ON_SURFACE)),
                top=BorderSide(4, colors.with_opacity(0.5, colors.ON_SURFACE)),
                right=BorderSide(4, colors.with_opacity(0.5, colors.ON_SURFACE)),
            ),
            left_axis=self.get_left_axis(self.get_total_story_points(self.sprint_tasks)),
            bottom_axis=self.get_bottom_axis(self.date_range),
            tooltip_bgcolor=colors.with_opacity(0.5, colors.GREY),
            tooltip_rounded_radius=10,
            horizontal_grid_lines=ChartGridLines(width=1, color=colors.with_opacity(0.5, colors.ON_SURFACE), interval=1),
            vertical_grid_lines=ChartGridLines(width=1, color=colors.with_opacity(0.5, colors.ON_SURFACE), interval=1),
            min_y=0,
            min_x=1,
        )
        
        return Container(
            content=chart,
            width=self.page.width * 0.7,
            height=self.page.height * 0.7,
            padding=padding.only(20, 20, 50, 20),
        )

    def get_completed_tasks_for_sprint(self):
        items = self.sprint_tasks
        # Filter out completed tasks
        completed_tasks = [item for item in items if item['status'] == 'Completed']
        return completed_tasks
    
    def get_sprint_dates(self):
        start_date = None
        end_date = None

        if 'start_date' in self.sprint:
            start_date = datetime.strptime(self.sprint['start_date'], '%d-%m-%Y').date()
        else:
            print(f"Start date not found for sprint_id: {self.sprint_id}")

        if 'end_date' in self.sprint:
            end_date = datetime.strptime(self.sprint['end_date'], '%d-%m-%Y').date()
        else:
            print(f"End date not found for sprint_id: {self.sprint_id}")

        return start_date, end_date

    def aggregate_story_points_by_date(self):
        # Initialize a dictionary to store the total story points completed on each date
        start_date, end_date = self.get_sprint_dates()
        if not start_date or not end_date:
            return [],[]
        
        all_tasks = self.sprint_tasks

        total_story_points = 0
        for task in all_tasks:
            total_story_points += int(task.get('story_points', 0))

        task_data = []

        completed_tasks = self.get_completed_tasks_for_sprint()
        for task in completed_tasks:
            date_value = self.date_to_value(datetime.strptime(task['date_completed'], '%d-%m-%Y').date())
            story_points = int(task.get('story_points', 0))
            task_data.append((date_value, story_points))
        
        # Sort the dates and calculate remaining points
        task_data.sort()
        remaining_points = total_story_points

        burndown_data = [(self.date_to_value(start_date), total_story_points)]

        for task in task_data:
            remaining_points -= task[1]
            burndown_data.append((task[0], remaining_points))

        ideal_burndown_data = [
            (self.date_to_value(start_date), total_story_points),
            (self.date_to_value(end_date), 0)
        ]   

        return burndown_data, ideal_burndown_data

