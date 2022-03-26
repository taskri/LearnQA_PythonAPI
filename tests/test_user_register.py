import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import pytest
from random import choices
import string

# python -m pytest -s tests/test_user_register.py -k test_create_user_successfully
# python -m pytest -s tests/test_user_register.py -k test_create_user_with_existing_email

# Homework: ex. 15 Test user method
# python -m pytest -s tests/test_user_register.py -k test_create_user_with_invalid_email
# python -m pytest -s tests/test_user_register.py -k test_create_user_with_one_field_missing
# python -m pytest -s tests/test_user_register.py -k test_name_fields_lengths_while_user_creation



class TestUserRegister(BaseCase):
    missing_fields = [
        "password",
        "username",
        "firstName",
        "lastName",
        "email"
    ]

    lengths = [
        1,
        251
    ]

    names = [
        "firstName",
        "lastName"
    ]

    def setup(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_invalid_email(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        data["email"] = data["email"].replace("@", "")

        response = requests.post("https://playground.learnqa.ru/api/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

    @pytest.mark.parametrize("missing_field", missing_fields)
    def test_create_user_with_one_field_missing(self, missing_field):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        data.pop(missing_field)

        response = requests.post("https://playground.learnqa.ru/api/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_field}"

    @pytest.mark.parametrize("length", lengths)
    @pytest.mark.parametrize("name", names)
    def test_name_fields_lengths_while_user_creation(self, length, name):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        source_for_name = string.ascii_letters + string.digits
        rand_name = "".join(choices(source_for_name, k=length))

        data[name] = rand_name

        response = requests.post("https://playground.learnqa.ru/api/user", data=data)

        if length < 2:
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The value of '{name}' field is too short"

        if length > 250:
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The value of '{name}' field is too long"





