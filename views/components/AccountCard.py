from flet import *
from data.manage_data import Data
import asyncio

from data.manage_user_data import UserData

class AccountCard(Container):
    def __init__(self, close_form, page, account_dict, handle_detailed_view=None):
        print("Account card initialized")
        super().__init__()

        self.page = page
        self.id = account_dict["_id"]
        self.username = account_dict["username"]
        self.password = account_dict["password"]  
        self.account_type = account_dict["account_type"]
        
        self.handle_detailed_view = handle_detailed_view
        self.close_form = close_form

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
        print("Account card clicked")

    
    def card_details(self):
        if self.page.current_user_info["account_type"] == "admin" and self.username == self.page.current_user_info["username"]:
            body = [
                self.username_details(),
                self.password_details(),
                Text(" ", color="black", size=20),
            ]
        elif self.page.current_user_info["account_type"] == "admin":
            body = [
                self.username_details(),
                self.password_details(),
                self.remove_account(),
            ]
        else:
            body = [
                self.username_details(),
            ]

        return Row(body,
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
            Text("Password: ", color="black", size=25),
            TextField(password=True, can_reveal_password=True, value=self.password, read_only=True, text_size=23, border=InputBorder.NONE, width=250),
        ],
        alignment=MainAxisAlignment.START)
        return password_column
    
    def remove_account(self):
        return Row([
            ElevatedButton(
                "Remove",
                bgcolor=colors.RED_200,
                on_click=lambda e: ((asyncio.run(UserData().remove_user(self.id))), self.close_form())
            )
        ],alignment=MainAxisAlignment.START)
