from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
from random import choices
import string
import allure


# python -m pytest -s tests/test_user_register.py -k test_create_user_successfully
# python -m pytest -s tests/test_user_register.py -k test_create_user_with_existing_email

# Homework: ex. 15 Test user method
# python -m pytest -s tests/test_user_register.py -k test_create_user_with_invalid_email
# python -m pytest -s tests/test_user_register.py -k test_create_user_with_one_field_missing
# python -m pytest -s tests/test_user_register.py -k test_name_fields_lengths_while_user_creation


@allure.epic("Registration cases")
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
        "username"  # ,
        # "firstName",
        # "lastName"
    ]

    @allure.title("Create user successfully")
    @allure.description("This test creates user successfully.")
    @allure.label("Positive/Negative", 'Positive')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Attempt to create a user with existing email")
    @allure.description("This test checks user creation with existing email.")
    @allure.label("Positive/Negative", 'Negative')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_decoded_content(response, f"Users with email '{email}' already exists")

    @allure.title("Attempt to create a user with invalid email")
    @allure.description("This test checks user creation with invalid email w/o @ symbol.")
    @allure.label("Positive/Negative", 'Negative')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_invalid_email(self):
        data = self.prepare_registration_data()

        data["email"] = data["email"].replace("@", "")

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_decoded_content(response, f"Invalid email format")

    @allure.description("This test checks user creation when one field is missing.")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("Positive/Negative", 'Negative')
    @allure.title("Attempt to create a user with missing field: {missing_field}")
    @pytest.mark.parametrize("missing_field", missing_fields)
    def test_create_user_with_one_field_missing(self, missing_field):
        data = self.prepare_registration_data()

        data.pop(missing_field)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_decoded_content(response, f"The following required params are missed: {missing_field}")

    @allure.title("Register with parametrized name with length: {length}")
    @allure.description("This test checks user creation with invalid name lengths.")
    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.label("Positive/Negative", 'Negative')
    @pytest.mark.parametrize("length", lengths)
    @pytest.mark.parametrize("name", names)
    def test_name_fields_lengths_while_user_creation(self, length, name):
        data = self.prepare_registration_data()

        source_for_name = string.ascii_letters + string.digits
        rand_name = "".join(choices(source_for_name, k=length))

        data[name] = rand_name

        response = MyRequests.post("https://playground.learnqa.ru/api/user", data=data)

        if length < 2:
            Assertions.assert_code_status(response, 400)
            Assertions.assert_decoded_content(response, f"The value of '{name}' field is too short")

        if length > 250:
            Assertions.assert_code_status(response, 400)
            Assertions.assert_decoded_content(response, f"The value of '{name}' field is too long")
