import asyncio
import json
from datetime import datetime
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
from flet import *
from data.manage_sprint_data import SprintData
from data.manage_data import Data


class BurndownChartPopup:
    def __init__(self, sprint_id, page):
        self.page = page
        self.sprint_id = sprint_id
        self.data_api = Data()
        self.sprint_data_api = SprintData()
        matplotlib.use("svg")

    async def get_completed_tasks_for_sprint(self, sprint_id):
        # items = asyncio.run(SprintData().get_sprint_items())
        items = await self.data_api.get_product_backlog_items()  # Await the coroutine


        # Filter out completed tasks
        # completed_tasks = [item for item in items if item['status'] == 'Completed']
        # return completed_tasks
    
        # sprint_id = 
        completed_tasks = [
            item for item in items 
            if item['sprint_id'] == sprint_id and item['status'] == 'Completed'
        ]
        return completed_tasks
    
    async def get_sprint_dates(self, sprint_id):
        sprint_item = await self.sprint_data_api.get_sprint_item(sprint_id)

        if sprint_item is None:
            print(f"No sprint item found for sprint_id: {sprint_id}")
            return None, None

        start_date = None
        end_date = None

        if 'start_date' in sprint_item:
            start_date = datetime.strptime(sprint_item['start_date'], '%d-%m-%Y')
        else:
            print(f"Start date not found for sprint_id: {sprint_id}")

        if 'end_date' in sprint_item:
            end_date = datetime.strptime(sprint_item['end_date'], '%d-%m-%Y')
        else:
            print(f"End date not found for sprint_id: {sprint_id}")

        return start_date, end_date

    async def aggregate_story_points_by_date(self, completed_tasks):
        # Initialize a dictionary to store the total story points completed on each date
        date_points = {}
        start_date, end_date = await self.get_sprint_dates(self.sprint_id)
        if not start_date or not end_date:
            return [],[]

        total_story_points = 0
        for task in completed_tasks:
            total_story_points += int(task.get('story_points', 0))

        burndown_data = []

        for task in completed_tasks:
            completed_date = datetime.strptime(task['date_completed'], '%d-%m-%Y').date()
            story_points = int(task.get('story_points', 0))

            if completed_date:
                if completed_date in date_points:
                    date_points[completed_date] += story_points
                else:
                    date_points[completed_date] = story_points
        
        # Sort the dates and calculate remaining points
        sorted_dates = sorted(date_points.keys())
        remaining_points = total_story_points

        if sorted_dates:  # Check if there are any sorted dates
            burndown_data.insert(0, (start_date, total_story_points))

        for date in sorted_dates:
            remaining_points -= date_points[date]
            burndown_data.append((date, remaining_points))

        ideal_burndown_data = [
        (start_date, total_story_points),
        (end_date, 0)
        ]   

        return burndown_data, ideal_burndown_data

    def generate_burndown_chart(self, burndown_data, ideal_burndown_data):
        # Plot the burndown chart
        plt.figure(figsize=(10, 6))

        if burndown_data:
            # Extract dates and remaining points for plotting
            dates = [entry[0] for entry in burndown_data]
            remaining_points = [entry[1] for entry in burndown_data]

            plt.plot(dates, remaining_points, marker='o', linestyle='-', color='b', label='Remaining Points')
            plt.fill_between(dates, remaining_points, color='blue', alpha=0.1)

        ideal_dates = [entry[0] for entry in ideal_burndown_data]
        ideal_remaining_points = [entry[1] for entry in ideal_burndown_data]

        plt.plot(ideal_dates, ideal_remaining_points, marker='o', linestyle='--', color='g', label='Ideal Line')

        # Formatting the chart
        plt.title('Burndown Chart')
        plt.xlabel('Date')
        plt.ylabel('Remaining Story Points')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.legend()
        # plt.show()

        # img_path = 'burndown_chart.png'  # Path where the image will be saved
        # plt.savefig(img_path, format='png')
        # plt.close()  # Close the plot to free memory

        # return img_path 
        return MatplotlibChart(figure=plt.gcf())
        
        

    async def display_burndown_chart(self, sprint_id):
        # Get completed tasks for the sprint
        completed_tasks = await self.get_completed_tasks_for_sprint(sprint_id)

        # Aggregate the story points by date
        burndown_data, ideal_burndown_data = await self.aggregate_story_points_by_date(completed_tasks)

        # Generate and show the burndown chart
        img_path = self.generate_burndown_chart(burndown_data, ideal_burndown_data)

        if img_path:
            # Create an Image component using the saved file path
            img_component = Image(src=img_path, width=600, height=400)
            dialog = AlertDialog(
                title = Text("Burndown Chart"),
                # content= img_component,
                content=self.generate_burndown_chart(burndown_data, ideal_burndown_data),
                actions= [
                TextButton("Close", on_click=lambda e: self.page.close(dialog))
            ],
            )

            self.page.open(dialog)

# async def main():
    
#     # Create an instance of BurndownChartPopup
#     burndown_chart_popup = BurndownChartPopup()

#     sprint_id = "sprint_id"

#     await burndown_chart_popup.display_burndown_chart(sprint_id)

# asyncio.run(main())
