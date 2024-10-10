import flet as ft
from flet import *
from data.manage_user_data import UserData
import asyncio

class LoginPage(Column):
    def __init__(self, page, on_login_success):
        super().__init__()
        self.page = page
        self.on_login_success = on_login_success
        self.bgcolor = "#DBEBE2"

        self.page.on_resized = lambda e: (print("Window resized"), self.page.update())

        self.username = TextField(label='Username', text_align = ft.TextAlign.CENTER, width = 400)
        self.password = TextField(label='Password', text_align = ft.TextAlign.CENTER, width = 400, password=True,can_reveal_password=True)
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
                    Container(height=20),
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
            height=420,
            alignment=ft.alignment.center,
        )

        self.controls = [
            Container(
                content=Column(
                        controls=[
                            Text("Welcome back! 🥳",size=40,weight="bold",text_align=ft.TextAlign.CENTER),
                            self.container],
                        alignment=ft.MainAxisAlignment.CENTER,  # Center vertically
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Center horizontally
                    ),
                width=self.page.width,
                height=self.page.height,
                # alignment=ft.MainAxisAlignment.CENTER,  # Cente·r horizontally
            ),
        ]

    def login(self, e):
        username = self.username.value
        password =self.password.value

        user_info = asyncio.run(UserData().get_user(username))
        # user_document = user_info['document']
        
        if user_info and user_info.get("password") == password:
            print("Login successful!")
            self.page.current_user_info = user_info
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

 
    def before_update(self):
        try:
            if self.page:
                self.controls[0].width = self.page.width
                self.controls[0].height =  self.page.height
                        
        except Exception as e:
            print(e)

