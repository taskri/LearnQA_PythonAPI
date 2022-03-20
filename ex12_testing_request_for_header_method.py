import requests


class TestRequestCookieMethod:
    def test_request_cookie_method(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        headers = response.headers
        print(headers)
        secret_header = {'x-secret-homework-header': 'Some secret value'}
        success_flag = False
        for key1 in headers:
            if key1 == "x-secret-homework-header":
                if headers[key1] == secret_header["x-secret-homework-header"]:
                    success_flag += True
                    break
        assert success_flag, "No special header in your homework."

#python -m pytest -s ex12_testing_request_for_header_method.py

