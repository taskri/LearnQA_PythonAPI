import requests

response = requests.get(" https://playground.learnqa.ru/api/long_redirect")

redirects_count = 0
for redirects in response.history:
    redirects_count += 1

print("Total number of redirects: " + str(redirects_count))

result_url = response.url
print("The result URL is " + result_url)
