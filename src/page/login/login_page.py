import pytest
from playwright.sync_api import Page
from utils.helpers import json_reader



class LoginPage:
    def __init__(self,page:Page,json_reader: json_reader):
        self.user_name=page.locator(json_reader["userEmail"])
        self.password=page.locator(json_reader["userPassword"])
        self.loginButton=page.locator(json_reader["login"])


    def login(self,user_name:str,password:str)->None:
        self.user_name.fill(user_name)
        self.password.fill(password)
        self.loginButton.click()


