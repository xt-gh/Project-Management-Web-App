# import flet as ft
# from flet import *
# from data.manage_sprint_data import SprintData
# from data.manage_data import Data

# class BarChartPopup(AlertDialog):
#     def __init__(self, page):
#         print("Bar chart pop up")
#         super().__init__()
#         self.page = page
#         self.modal = True  # Ensures it's a modal dialog (focus stays on dialog)
#         self.width = 600
#         self.height = 400
#         self.content = self.build_popup_content()

#     def build_popup_content(self):
#         # Bar chart creation (same as before)
#         chart = ft.BarChart(
#             bar_groups=[
#                 ft.BarChartGroup(
#                     x=0,
#                     bar_rods=[
#                         ft.BarChartRod(
#                             from_y=0,
#                             to_y=40,
#                             width=40,
#                             color=ft.colors.AMBER,
#                             tooltip="Apple",
#                             border_radius=0,
#                         ),
#                     ],
#                 ),
#                 ft.BarChartGroup(
#                     x=1,
#                     bar_rods=[
#                         ft.BarChartRod(
#                             from_y=0,
#                             to_y=100,
#                             width=40,
#                             color=ft.colors.BLUE,
#                             tooltip="Blueberry",
#                             border_radius=0,
#                         ),
#                     ],
#                 ),
#                 ft.BarChartGroup(
#                     x=2,
#                     bar_rods=[
#                         ft.BarChartRod(
#                             from_y=0,
#                             to_y=30,
#                             width=40,
#                             color=ft.colors.RED,
#                             tooltip="Cherry",
#                             border_radius=0,
#                         ),
#                     ],
#                 ),
#                 ft.BarChartGroup(
#                     x=3,
#                     bar_rods=[
#                         ft.BarChartRod(
#                             from_y=0,
#                             to_y=60,
#                             width=40,
#                             color=ft.colors.ORANGE,
#                             tooltip="Orange",
#                             border_radius=0,
#                         ),
#                     ],
#                 ),
#             ],
#             border=ft.border.all(1, ft.colors.GREY_400),
#             left_axis=ft.ChartAxis(
#                 labels_size=40, title=ft.Text("The Specific User"), title_size=40
#             ),
#             bottom_axis=ft.ChartAxis(
#                 labels=[
#                     ft.ChartAxisLabel(
#                         value=0, label=ft.Container(ft.Text("Date1"), padding=10)
#                     ),
#                     ft.ChartAxisLabel(
#                         value=1, label=ft.Container(ft.Text("Date2"), padding=10)
#                     ),
#                     ft.ChartAxisLabel(
#                         value=2, label=ft.Container(ft.Text("Date3"), padding=10)
#                     ),
#                     ft.ChartAxisLabel(
#                         value=3, label=ft.Container(ft.Text("Date4"), padding=10)
#                     ),
#                 ],
#                 labels_size=40,
#             ),
#             horizontal_grid_lines=ft.ChartGridLines(
#                 color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
#             ),
#             tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
#             max_y=110,
#             interactive=True,
#             expand=True,
#         )

#         # Close button
#         close_button = ft.ElevatedButton(
#             text="Close",
#             on_click=self.close_popup,  # Event handler to close the dialog
#             bgcolor=ft.colors.RED
#         )

#         # Combine the chart and close button in a Column layout
#         return ft.Column(
#             [
#                 chart,
#                 close_button  # Add the close button below the chart
#             ],
#             alignment=ft.MainAxisAlignment.CENTER
#         )

#     def close_popup(self, e):
#         # Close the popup by setting its open attribute to False and updating the page
#         self.open = False
#         self.page.update()

import flet as ft
from flet import *

class BarChartPopup(AlertDialog):
    def __init__(self, page, specific_username):
        print("Bar chart pop up")
        super().__init__()
        self.page = page
        self.specific_username = specific_username
        self.modal = True  # Ensures it's a modal dialog (focus stays on dialog)
        self.width = 600  # Fixed width of the popup window
        self.height = 600  # Fixed height of the popup window
        self.content = self.build_popup_content()

    def build_popup_content(self):
        num_bars = 4
        bar_width = 40  # Width of each bar
        spacing = 100    # Space between bars
        total_width = num_bars * (bar_width + spacing) - spacing  # Total width needed for the bars

        # Create a list of bar groups with x positions adjusted for spacing
        bar_groups = []
        for i in range(num_bars):
            bar_groups.append(
                ft.BarChartGroup(
                    x=i * (bar_width + spacing),  # Adjust the x position with spacing
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=(i + 1) * 20,  # Example values; adjust as needed
                            width=bar_width,  # Width of the bar
                            color=[ft.colors.AMBER, ft.colors.BLUE, ft.colors.RED, ft.colors.ORANGE][i],
                            tooltip = f"Date{i+1}",
                            border_radius=0,
                            
                        ),
                    ],
                )
            )

        # Bar chart creation
        chart = ft.BarChart(
            bar_groups=bar_groups,
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels_size=40, title=ft.Text("Total hours of contribution"), title_size=40
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=i * (bar_width + spacing), label=ft.Container(ft.Text(f"Date{i + 1}"), padding=10)
                    )
                    for i in range(num_bars)
                ],
                labels_size=40, title=ft.Text("Date"), title_size=40
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
            max_y=100,  # Adjust as needed based on data
            interactive=True,
            expand=True,  # Allow the chart to expand and fill the popup
        )

        # Title for the chart
        title = ft.Text(
            self.specific_username,  # Set your title here
            size=24,  # Set the font size
            weight=ft.FontWeight.BOLD,  # Make the title bold
        )

        # Close button
        close_button = ft.ElevatedButton(
            content=Text("Close", color="black"),
            on_click=self.close_popup,  # Event handler to close the dialog
            bgcolor=colors.RED_100,
        )

        # Combine the chart and close button in a Column layout
        return ft.Column(
            [
                title,
                chart,
                close_button  # Add the close button below the chart
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            width = self.width,
            height = self.height,
        )

    def close_popup(self, e):
        print("Close bar chart pop-up")
        # Close the popup by setting its open attribute to False and updating the page
        self.open = False
        self.page.update()