import json.decoder
from datetime import datetime
from requests import Response
from lib.my_requests import MyRequests
from lib.assertions import Assertions
import allure


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with the name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with the name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def edit_user_data(self, user_id, field_to_edit, new_value, auth_data: dict = None):

        if auth_data == None:
            with allure.step("Get user details w/o auth data."):
                response = MyRequests.put(
                    f"/user/{user_id}",
                    data={field_to_edit: new_value}
                )

            return response
        with allure.step("Get user details with auth data."):
            response = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": auth_data["token"]},
                cookies={"auth_sid": auth_data["auth_sid"]},
                data={field_to_edit: new_value}
            )

        return response

    def register_new_user(self):
        register_data = self.prepare_registration_data()
        with allure.step(f"Create a new user with register data: {register_data}"):
            response = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        new_user_data = {
            "email": register_data["email"],
            "password": register_data["password"],
            "user_id": self.get_json_value(response, "id")
        }

        return new_user_data

    def login(self, login_data: dict):
        with allure.step(f"Login with this data: {login_data}"):
            response = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_code_status(response, 200), "User is not authenticated"

        auth_data = {
            "auth_sid": self.get_cookie(response, "auth_sid"),
            "token": self.get_header(response, "x-csrf-token")
        }

        return auth_data

    def get_current_user_info(self, user_data: dict):

        with allure.step(f"Authenticate with this data: {user_data}"):
            auth_data = self.login(user_data)

        with allure.step(f"Get user info of current user: {user_data['user_id']}"):
            response = MyRequests.get(f"/user/{user_data['user_id']}",
                                      headers={"x-csrf-token": auth_data["token"]},
                                      cookies={"auth_sid": auth_data["auth_sid"]})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response, expected_fields)

        response_as_dict = response.json()

        return response_as_dict

    def delete_user(self, user_id, auth_data):
        with allure.step(f"Delete user with id: {user_id}"):
            response = MyRequests.delete(f"/user/{user_id}", headers={"x-csrf-token": auth_data["token"]},
                                         cookies={"auth_sid": auth_data["auth_sid"]})
        return response
