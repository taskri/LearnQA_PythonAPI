import requests


class TestRequestCookieMethod:
    def test_request_cookie_method(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        assert requests.cookies, "No cookie in response."
        cookie_in_request = response.cookies
        print(cookie_in_request)
        str_cookie_in_request = str(cookie_in_request)
        expected_cookie = "<RequestsCookieJar[<Cookie HomeWork=hw_value for .playground.learnqa.ru/>]>"
        assert expected_cookie == str_cookie_in_request, "Cookies in response are differ the expected ones."

#python -m pytest -s ex11_testing_request_for_cookie_method.py

