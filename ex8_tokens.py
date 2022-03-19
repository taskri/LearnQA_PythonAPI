import requests
import json
import time

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
parsed_json = json.loads(response.text)

if "token" in parsed_json:
    token = {"token": parsed_json["token"]}
    response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token)
    parsed_json_job_status = json.loads(response.text)
    if parsed_json_job_status["status"] == "Job is NOT ready":
        print("The status field is all right! Check it: \"{status}\".".format(status=parsed_json_job_status["status"]))
        print()

if "token" in parsed_json and "seconds" in parsed_json:
    print("Please, wait for {seconds} seconds.".format(seconds=parsed_json["seconds"]))
    print()
    time.sleep(parsed_json["seconds"])
    response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token)
    parsed_json_job_status = json.loads(response.text)
    if parsed_json_job_status["status"] == "Job is ready":
        print("The status field is all right! Check it: \"{status}\".".format(status=parsed_json_job_status["status"]))
        if "result" in parsed_json_job_status:
            print("There's the result of the job: {result}.".format(result=parsed_json_job_status["result"]))
