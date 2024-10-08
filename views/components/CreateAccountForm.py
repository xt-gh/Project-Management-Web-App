from flet import *
import asyncio
import re
from .FormComponents import DropdownInput, TextFieldInput, MultipleSelectInput, TextFieldDatePicker
from data.manage_user_data import UserData


class CreateAccountForm(AlertDialog):
    def __init__(self,page,close_form, mode="create account", account_dict=None):
        super().__init__()
        self.page = page
        self.close_form = close_form
        self.mode = mode  # Mode can be "add" or "view" or "edit"
        self.account_dict = account_dict
        self.content_padding = 10
        self.inset_padding = 10
        self.bgcolor = "#CADEED"
        self.clip_behavior = ClipBehavior.HARD_EDGE

        # build form content
        self.content = self.build_create_account_form()
        self.inset_padding = 10
        self.actions_padding = 20

    
    def build_create_account_form(self):
        self.username = TextFieldInput(label="User Email", is_required=True)
        self.password = TextFieldInput(label="Password", is_required=True)
        self.actions = [
            ElevatedButton("Cancel", bgcolor=colors.RED_300, width=100,color="black",on_click= lambda e: self.close_form()),
            ElevatedButton("Save", bgcolor=colors.GREEN_300, width=100,color="black",on_click= lambda e: self.handle_submit()),
        ]

        if self.mode == "create account":
            self.header = [Text("Create New Account", color="black", size=24)]
        else:
            self.header = [Text("Account information", color="black", size=24)]

            # self.username.value = "username"
            # self.password.value = "password"

        return Container(
            content=Column(
                [
                    Row(self.header, alignment=MainAxisAlignment.SPACE_BETWEEN),

                    Row([
                        # Container(Text("Username:", color="black", size=15),padding=padding.only(0, 0, 5, 0), expand=1),
                        Container(self.username, padding=padding.only(5, 0, 0, 0), expand=1),
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),

                    Row([
                        # Container(Text("Password:", color="black", size=15),padding=padding.only(0, 0, 5, 0), expand=1),
                        Container(self.password, padding=padding.only(5, 0, 0, 0), expand=1),
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),

                    Text("At least an uppercase letter.", color="black", size=20),
                    Text("At least an lowercase letter.", color="black", size=20),
                    Text("At least a number.", color="black", size=20),
                    Text("At least a unique symbol.", color="black", size=20),
                    Text("At least 8 characters.", color="black", size=20),
                ],
                on_scroll=lambda e: print("Scrolled"),
                scroll=ScrollMode.AUTO,
                alignment=MainAxisAlignment.START,
            ),
            width=self.page.width * 0.2,
            height=self.page.height * 0.4,
            padding=padding.only(15, 15, 15, 15),
            border_radius=border_radius.all(10),
            expand=1
        )
    
    def is_valid_form(self):
        is_valid = True

        if self.username.value.strip() == "":
            is_valid = False

        if self.password.value.strip() == "":
            is_valid = False

        return is_valid
    
    def are_password_valid(self):
        password = self.password.value
        password_isvalid = True
        message = "Password is valid."

        # Check length
        if len(password) < 8:
            password_isvalid = False
            message = "Password must be at least 8 characters long."

        # Check for uppercase letter
        if not re.search(r"[A-Z]", password):
            password_isvalid = False
            message = "Password must contain at least one uppercase letter."

        # Check for lowercase letter
        if not re.search(r"[a-z]", password):
            password_isvalid = False
            message = "Password must contain at least one lowercase letter."

        # Check for digit
        if not re.search(r"\d", password):
            password_isvalid = False
            message = "Password must contain at least one digit."

        # Check for special symbol
        if not re.search(r"[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", password):
            password_isvalid = False
            message = "Password must contain at least one special symbol."

        return password_isvalid, message
    
    def handle_submit(self):
        if self.is_valid_form():
            print("Form is valid")
        
            # Check if password is valid
            password_isvalid, message = self.are_password_valid()

            if not password_isvalid:
                # Show an error message if the password is invalid
                self.password.error_text = message
                self.page.update()
                return  # Stop submission if password is invalid

            user_account = {
                "username": self.username.value,
                "password": self.password.value,
                "account_type": "standard",
            }


            if self.mode == "create account":
                asyncio.run(UserData().add_user(user_account))

            else:
                asyncio.run(UserData().update_user_info(account_id=self.account_dict["_id"], updated_fields=user_account))
            self.close_form()
    
        else:
            if self.username.value.strip() == "":
                self.username.error_text = "Username is required"
            if self.password.value.strip() == "":
                self.username.error_text = "Password is required"

        self.page.update()


