from flet import *

class TaskLogTable(DataTable):
    def __init__(self, log_list, **kwargs):
        self.columns = [
            DataColumn(Text("User", color="black", size=15)),
            DataColumn(Text("Date", color="black", size=15)),
            DataColumn(Text("Time", color="black", size=15)),
            DataColumn(Text("Action", color="black", size=15)),
        ]
        super().__init__(columns=self.columns, **kwargs)
        print("TaskLogTable initialized", log_list)

        self.bgcolor = "#CADEED"
        self.border = border.all(1, "#000000")
        self.border_radius = 10

        if len(log_list) > 0:
            self.rows = [
                DataRow(
                    cells=[
                        DataCell(Text(log["user"], color="black", size=15)),
                        DataCell(Text(log["date"], color="black", size=15)),
                        DataCell(Text(log["time"], color="black", size=15)),
                        DataCell(Text(log["action"], color="black", size=15)),
                    ]
                )
                for log in log_list
            ]

        else:
            self.rows = [
                DataRow(
                    cells=[
                        DataCell(Text("-", color="black", size=15)),
                        DataCell(Text("-", color="black", size=15)),
                        DataCell(Text("-", color="black", size=15)),
                        DataCell(Text("-", color="black", size=15)),
                    ]
                )
            ]
