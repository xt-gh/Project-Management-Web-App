from flet import *
from data.manage_data import Data
import asyncio

from data.manage_user_data import UserData

class AccountCard(Container):
    def __init__(self, page, account_dict, handle_detailed_view=None):
        print("Account card initialized")
        super().__init__()

        self.page = page
        self.id = account_dict["_id"]
        self.username = account_dict["username"]
        self.password = account_dict["password"]  
        self.account_type = account_dict["account_type"]
        
        self.handle_detailed_view = handle_detailed_view

        self.bgcolor = "#BABDE2"
        self.border = border.all(1.5, "#000000")
        self.border_radius = border_radius.all(10)
        self.padding = padding.all(10)
        self.margin = margin.all(3)
        self.expand = 1
        self.ink = True
        self.on_click = lambda e: self.handle_on_click()
        self.content = self.card_details()
        self.height = 80

    def handle_on_click(self):
        self.handle_detailed_view(self.id)

    # def card_title(self):
    #     return Row([
    #         Text(
    #             f"{self.username}",
    #             color="black", 
    #             size=15,
    #             weight=FontWeight.BOLD,
    #             max_lines=2,
    #             expand=1,
    #             overflow=TextOverflow.ELLIPSIS
    #         ),
    #         # IconButton(
    #         #     icon=icons.REMOVE,
    #         #     icon_color="black",
    #         #     icon_size=30,
    #         #     on_click=lambda e: self.handle_detailed_view(self.id),
    #         #     hover_color="#F1F1F1",
    #         #     # disabled=self.status != "Not Started",
    #         #     # mouse_cursor=MouseCursor.CLICK if self.status == "Not Started" else MouseCursor.FORBIDDEN,
    #         # )
    #     ],alignment=MainAxisAlignment.SPACE_BETWEEN)
    
    def card_details(self):
        return Row([
            self.username_details(),
            self.remove_account()
        ],
        alignment=MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=CrossAxisAlignment.CENTER)
    
    def username_details(self):
        
        username_column = Row([
            Icon(name=icons.PERSON),
            Text("Username: " + self.username, color="black", size=25),
        ],
        alignment=MainAxisAlignment.START)
    
        # We need a new field for each account, "account_type"
        if self.account_type == "admin":
            username_column.controls.append(Text("(Admin)", color="red", size=20))
        return username_column
    
    def password_details(self):
        password_column = Row([
            Text("Password: " + self.password, color="black", size=25),
        ],
        alignment=MainAxisAlignment.START)
        return password_column
    
    def remove_account(self):
        return Row([
            ElevatedButton(
                "Remove",
                bgcolor=colors.RED_200,
                on_click=lambda e: (asyncio.run(UserData().remove_user_account_item(self.account_dict["_id"]))),
            )
        ],alignment=MainAxisAlignment.START)
    
