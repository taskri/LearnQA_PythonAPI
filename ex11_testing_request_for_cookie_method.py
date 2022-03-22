import requests


class TestRequestCookieMethod:
    def test_request_cookie_method(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        assert requests.cookies, "No cookie in response."
        print(response.cookies)
        assert response.cookies.get("HomeWork"), "No 'HomeWork' cookie in response."
        cookie_in_request = response.cookies.get("HomeWork")
        expected_cookie = {"HomeWork": "hw_value"}
        assert expected_cookie["HomeWork"] == cookie_in_request, "Cookies from the response differ the expected ones."

#python -m pytest -s ex11_testing_request_for_cookie_method.py

