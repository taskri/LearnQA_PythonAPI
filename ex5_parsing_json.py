import json

text_json = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
parsed_json = json.loads(text_json)

"""
#Print the second message without any check:
print(parsed_json["messages"][1]["message"])

#Values for a task:
key1 = "messages"
key2 = 1
key3 = "message"
"""

key1 = "messages"
key2 = 1
key3 = "message"

if key1 in parsed_json:
    list_length = len(parsed_json[key1])
    if key2 + 1 <= list_length:
        if key3 in parsed_json[key1][key2]:
            print(parsed_json[key1][key2][key3])
        else:
            print(f"No {key3} in the {key2+1} list entry.")
    else:
        print(f"There's less than {key2+1} entries in the list with messages.")
else:
    print(f"There's no {key1} in the JSON string.")
