import flet as ft
from flet import *
from data.manage_user_data import UserData
import asyncio

class LoginPage(Column):
    def __init__(self, page, on_login_success):
        super().__init__()
        self.page = page
        self.on_login_success = on_login_success

        
        self.username = TextField(label='Username', text_align = ft.TextAlign.LEFT, width = 200)
        self.password = TextField(label='Password', text_align = ft.TextAlign.LEFT, width = 200, password=True)
        self.login_button = ElevatedButton(text='Log In', width = 200, disabled=True, on_click=self.login)
        self.login_result = Text("")

        def validate(e):
            if all([self.username.value, self.password.value]):
                self.login_button.disabled = False
            else:
                self.login_button.disabled = True

            page.update()

        self.username.on_change = validate
        self.password.on_change = validate

        self.controls = [
            self.username,
            self.password,
            self.login_button,
            self.login_result
        ]

    def login(self, e):
        username = self.username.value
        password =self.password.value

        user_info = asyncio.run(UserData().get_user(username))
        
        if user_info and user_info.get("password") == password:
            print("Login successful!")
            self.page.user = user_info.get("account_type")
            self.on_login_success()  # Call the success callback
        elif user_info == None:
            print("Login failed! User not found.")
            self.login_result.value = "Login failed! User not found."  # Update login result
            self.login_result.color = "red"
        else:
            print("Login failed! Incorrect password.")
            self.login_result.value = "Login failed! Incorrect password."  # Update login result
            self.login_result.color = "red"

        self.page.update()
