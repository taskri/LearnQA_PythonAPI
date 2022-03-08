import requests

# Task #1
print("Task #1")
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
# prints <Response [200]> "Wrong method provided"
print(response, response.text)
print("-----")

# Task #2
print("Task #2")
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
# prints <Response [400]> and no text
print(response, response.text)
print("-----")

# Task #3
print("Task #3")
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "POST"})
# prints <Response [200]> {"success":"!"}
print(response, response.text)
print("-----")

# Task #4
print("Task #4")
list_of_https_requests = ["GET", "POST", "PUT", "DELETE"]
wrong_combination = {}
right_comb_with_err_result = {}

for request_type in list_of_https_requests:
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": request_type})
    if response.text == '{"success":"!"}' and request_type != "GET":
        wrong_combination.update({"Used HTTP method": "GET", "Method in params": request_type, "Response text": '{"success":"!"}'})
    elif response.text == "Wrong method provided" and request_type == "GET":
        right_comb_with_err_result.update({"Used HTTP method": "GET", "Method in params": request_type, "Response text": "Wrong method provided"})
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": request_type})
    if response.text == '{"success":"!"}' and request_type != "POST":
        wrong_combination.update({"Used HTTP method": "POST", "Method in data": request_type, "Response text": '{"success":"!"}'})
    elif response.text == "Wrong method provided" and request_type == "POST":
        right_comb_with_err_result.update({"Used HTTP method": "POST", "Method in data": request_type, "Response text": "Wrong method provided"})
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": request_type})
    if response.text == '{"success":"!"}' and request_type != "PUT":
        wrong_combination.update({"Used HTTP method": "PUT", "Method in data": request_type, "Response text": '{"success":"!"}'})
    elif response.text == "Wrong method provided" and request_type == "PUT":
        right_comb_with_err_result.update({"Used HTTP method": "PUT", "Method in data": request_type, "Response text": "Wrong method provided"})
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": request_type})
    if response.text == '{"success":"!"}' and request_type != "DELETE":
        wrong_combination.update({"Used HTTP method": "DELETE", "Method in data": request_type, "Response text": '{"success":"!"}'})
    elif response.text == "Wrong method provided" and request_type == "DELETE":
        right_comb_with_err_result.update({"Used HTTP method": "DELETE", "Method in data": request_type, "Response text": "Wrong method provided"})

if wrong_combination != {}:
    print(wrong_combination)
if right_comb_with_err_result != {}:
    print(right_comb_with_err_result)


