import time

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

# python -m pytest tests/test_user_delete.py -k test_delete_default_user
# python -m pytest tests/test_user_delete.py -k test_delete_just_created_user
# python -m pytest tests/test_user_delete.py -k test_delete_user_as_another_user

@allure.epic("User deletion cases")
class TestUserDelete(BaseCase):
    TEST_CASE_LINK = "https://github.com/taskri/LearnQA_PythonAPI/blob/master/tests/test_user_delete.py"

    @allure.description("This test checks deletion of default user.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("Positive/Negative", 'Negative')
    def test_delete_default_user(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        auth_data = self.login(login_data)

        response = self.delete_user("2",auth_data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_decoded_content(response, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    @allure.description("This test creates a new user and deletes it successfully.")
    @allure.issue(TEST_CASE_LINK, "BUG")
    def test_delete_just_created_user(self):
        login_data = self.register_new_user()
        auth_data = self.login(login_data)

        response1 = self.delete_user(login_data["user_id"], auth_data)
        Assertions.assert_code_status(response1, 200)

        response2 = MyRequests.get(f"/user/{login_data['user_id']}")
        Assertions.assert_code_status(response2, 404)
        Assertions.assert_decoded_content(response2, "User not found")

    @allure.description("This test creates two users and checks deletion of the one user performed by another. As the "
                        "result, performer is deleted.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("Positive/Negative", 'Negative')
    @allure.testcase(TEST_CASE_LINK, "Test case link check")
    def test_delete_user_as_another_user(self):
        editor_login_data = self.register_new_user()
        auth_data = self.login(editor_login_data)
        time.sleep(1)

        target_of_deletion_login_data = self.register_new_user()

        response = self.delete_user(target_of_deletion_login_data["user_id"], auth_data)
        Assertions.assert_code_status(response, 200)

        response_check_target = MyRequests.get(f"/user/{target_of_deletion_login_data['user_id']}")
        Assertions.assert_code_status(response_check_target, 200)

        response_check_editor = MyRequests.get(f"/user/{editor_login_data['user_id']}")
        Assertions.assert_code_status(response_check_editor, 404)
        Assertions.assert_decoded_content(response_check_editor, "User not found")





