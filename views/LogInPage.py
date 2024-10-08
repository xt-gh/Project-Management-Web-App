import flet as ft
from flet import *
from data.manage_user_data import UserData
import asyncio

class LoginPage(Column):
    def __init__(self, page, on_login_success):
        super().__init__()
        self.page = page
        self.on_login_success = on_login_success

        self.username = TextField(label='Username', text_align = ft.TextAlign.CENTER, width = 400)
        self.password = TextField(label='Password', text_align = ft.TextAlign.CENTER, width = 400, password=True)
        self.login_button = ElevatedButton(
            text='Log In',
            width = 400,
            disabled=True,
            on_click=self.login,
            style=ButtonStyle(
                text_style=TextStyle(size=18)
            )
        )
        self.login_result = Text("")

        def validate(e):
            if all([self.username.value, self.password.value]):
                self.login_button.disabled = False
            else:
                self.login_button.disabled = True

            page.update()

        self.username.on_change = validate
        self.password.on_change = validate

        self.container = Container(
            content=Column(
                controls=[
                    Icon(name=ft.icons.PERSON,size=50,color="black"),
                    Text("LOG IN",size=30,weight="bold",text_align=ft.TextAlign.CENTER),
                    Text("Please enter your username and password to log in.",size=16,text_align=ft.TextAlign.CENTER),
                    self.username,
                    self.password,
                    Container(height=25),
                    self.login_button,
                    self.login_result
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing = 10,
            ),
            padding = 20,
            border_radius=15,
            bgcolor="#CADEED",
            width=500,
            height=390,
            alignment=ft.alignment.center,
        )

        self.controls = [
            Row(
                alignment=ft.MainAxisAlignment.CENTER,  # Center horizontally
                controls=[
                    Column(
                        controls=[
                            Text("Welcome back! 🥳",size=40,weight="bold",text_align=ft.TextAlign.CENTER),
                            self.container],
                        alignment=ft.MainAxisAlignment.CENTER,  # Center vertically
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Center horizontally
                    )
                ],
                height=self.page.window.height,  
            )
        ]

    def login(self, e):
        username = self.username.value
        password =self.password.value

        user_info = asyncio.run(UserData().get_user(username))
        
        if user_info and user_info.get("password") == password:
            print("Login successful!")
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


