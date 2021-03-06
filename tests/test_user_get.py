from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


# python -m pytest tests/test_user_get.py -k test_get_user_details_not_auth
# python -m pytest tests/test_user_get.py -k test_get_user_details_auth_as_the_same_user
# python -m pytest tests/test_user_get.py -k test_get_the_same_user_details_auth_as_another_user

@allure.epic("Get user details cases")
class TestUserGet(BaseCase):
    @allure.description("This test checks user details w/o authorization info")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")

        not_expected_values = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(response, not_expected_values)

    @allure.description("This test creates a new user and gets its info successfully.")
    @allure.label("Positive/Negative", 'Positive')
    def test_get_user_details_auth_as_the_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test checks getting only username of the same user with authorization info of another user.")
    def test_get_the_same_user_details_auth_as_another_user(self):
        data = {
            "email": "learnqa03272022134551@example.com",
            "password": "123"
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.get("/user/2",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_has_key(response2, "username")

        not_expected_values = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(response2, not_expected_values)
