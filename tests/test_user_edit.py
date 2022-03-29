import time
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


# python -m pytest tests/test_user_edit.py -k test_edit_just_created_user
# python -m pytest tests/test_user_edit.py -k test_edit_user_without_auth
# python -m pytest tests/test_user_edit.py -k test_edit_user_as_another_user
# python -m pytest tests/test_user_edit.py -k test_edit_email
# python -m pytest tests/test_user_edit.py -k test_edit_firstName
# python -m pytest tests/test_user_edit.py -k test_edit_just_created_user_with_invalid_values

@allure.epic("User edition cases")
class TestUserEdit(BaseCase):
    invalid_values = [
        [
            "email",
            "email_without_symbol.com"
        ],
        [
            "firstName",
            "A",
        ]
    ]
    @allure.description("This test creates a new user and edits its firstName successfully.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("Positive/Negative", 'Positive')
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        auth_data = {
            "auth_sid": auth_sid,
            "token": token
        }

        # EDIT
        new_name = "Changed name"

        response3 = self.edit_user_data(user_id, "firstName", new_name, auth_data)

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test checks editing user info of the same user w/o authorization info.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("Positive/Negative", 'Negative')
    def test_edit_user_without_auth(self):
        new_values = {
            'password': '123456',
            'username': 'editedUsername',
            'firstName': 'editedFirstName',
            'lastName': 'editedLastName',
            'email': "edited@email.com"
        }
        for field in new_values:
            response = self.edit_user_data("29629", field, new_values[field])
            Assertions.assert_code_status(response, 400)
            Assertions.assert_decoded_content(response, "Auth token not supplied")

    @allure.description("This test checks editing user info of a just created user by another one.")
    @allure.label("Positive/Negative", 'Negative')
    def test_edit_user_as_another_user(self):
        # USER CREATION
        user1 = self.register_new_user()
        time.sleep(1)
        user2 = self.register_new_user()

        user2_info = self.get_current_user_info(user2)

        # LOGIN AS THE FIRST USER
        auth_data1 = self.login(user1)

        # TRY TO EDIT ALL FIELDS OF THE SECOND USER
        new_values = {
            'password': '123456',
            'username': 'editedUsername',
            'firstName': 'editedFirstName',
            'lastName': 'editedLastName',
            'email': f"edited{user2['email']}"
        }

        for field in new_values:
            response = self.edit_user_data(user2["user_id"], field, new_values[field], auth_data1)
            Assertions.assert_code_status(response, 200)

        # CHECK THAT NO CHANGES WERE APPLIED
        assert user2_info == self.get_current_user_info(user2), f"User data has been changed by another user"


    @allure.description("This test checks editing 'email' field of the just created user with invalid email address w/o @ symbol.")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.label("Positive/Negative", 'Negative')
    def test_edit_email(self):
        login_data = self.register_new_user()
        auth_data = self.login(login_data)

        response = self.edit_user_data(login_data["user_id"], "email", "email_without_symbol.com", auth_data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_decoded_content(response, "Invalid email format")

    @allure.description("This test checks editing 'firstName' field of the just created user with invalid firts Name in one symbol.")
    @allure.label("Positive/Negative", 'Negative')
    def test_edit_firstName(self):
        login_data = self.register_new_user()
        auth_data = self.login(login_data)

        response = self.edit_user_data(login_data["user_id"], "firstName", "a", auth_data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_decoded_content(response, '{"error":"Too short value for field firstName"}')

    @allure.description("This test checks editing one field of the just created user with an invalid value.")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.label("Positive/Negative", 'Negative')
    @allure.title("Attempt to change field with invalid value: {invalid_value}")
    @pytest.mark.parametrize("invalid_value", invalid_values)
    def test_edit_just_created_user_with_invalid_values(self, invalid_value):

        login_data = self.register_new_user()
        auth_data = self.login(login_data)

        response = self.edit_user_data(login_data["user_id"], invalid_value[0], invalid_value[1], auth_data)
        Assertions.assert_code_status(response, 400)
        if invalid_value[0] == "email":
            Assertions.assert_decoded_content(response, "Invalid email format")
        elif len(invalid_value[1]) < 2:
            Assertions.assert_decoded_content(response, '{"error":"Too short value for field '+f'{invalid_value[0]}'+'"}')















