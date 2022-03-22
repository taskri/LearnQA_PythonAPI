import requests
import pytest


# python -m pytest -s ex13_user_agent.py


class TestUserAgent:
    data = [
        [
            'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}
        ],
        [
            'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
            {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}
        ],
        [
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}
        ],
        [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
            {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}
        ],
        [
            'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}
        ]
    ]
    values_to_check = ["platform", "browser", "device"]

    @pytest.mark.parametrize("data", data)
    @pytest.mark.parametrize("value_to_check", values_to_check)
    def test_user_agent(self, data, value_to_check):
        #print(data)

        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        response = requests.get(url, headers={"User-Agent": data[0]})
        assert response.json()[value_to_check], "No {value_to_check} in response.".format(value_to_check=value_to_check)

        #print()
        #print(response.json()[value_to_check], data[1][value_to_check])

        assert response.json()[value_to_check] == data[1][value_to_check], "The {value_to_check} from response is wrong.".format(value_to_check=value_to_check)
