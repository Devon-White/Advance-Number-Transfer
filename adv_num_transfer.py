# The purpose of this script to to transer numbers from one space to another and retain the number settings.

import base64
from time import sleep
import requests
import json

originating_number_list = []
receiving_number_list = []
new_list = []

from_space = input("What is the name of the originating SignalWire Space")
from_project = input("What is the Project ID of the originating Space?")
from_token = input("What is the Auth Token of the originating space?")

print("Originating Space credentials and numbers stored, please supply the receiving parties credentials...")
sleep(1)
to_space = input("What is the name of the receiving SignalWire Space")
to_project = input("What is the Project ID of the receiving Space?")
to_token = input("What is the Auth Token of the receiving space?")


def list_numbers(space, auth, lists):
    url = f"https://{space}.signalwire.com/api/relay/rest/phone_numbers"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {auth}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = response.json()
    data_parser(response_json, lists)


def encoding(key):
    key = key.encode("UTF-8")
    key_bytes = base64.b64encode(key)
    key_encoded = key_bytes.decode('UTF-8')
    return key_encoded


def data_parser(response_json, lists):
    for number in response_json['data']:
        if number['call_handler'] == 'laml_webhooks' or number['message_handler'] == 'laml_webhooks':
            lists.append({"data": number})
    return


def finalizer(auth):
    for number in originating_number_list:
        if number['data']['number'] not in new_list:
            current_number = number['data']['number']
            payload_list = {}
            for k, v in number['data'].items():
                if v is not None and v != "":
                    payload_list[k] = v
                    print(k, v)
                    if 'name' in payload_list:
                        pass
                    else:
                        payload_list['name'] = number['data']['number']
            for new_id in receiving_number_list:
                if current_number == new_id['data']['number'] and current_number not in new_list:
                    new_list.append(current_number)
                    ids = new_id['data']['id']
                    url = f'https://{to_space}.signalwire.com/api/relay/rest/phone_numbers/{ids}'
                    print(url)

                    payload = json.dumps(payload_list)
                    headers = {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Authorization': f'Basic {auth}'
                    }

                    response = requests.request("PUT", url, headers=headers, data=payload)
                    print(response.text)
                    print(payload)
                    finalizer(auth)
                    print(payload_list)


def confirmation():
    z = input(
        f"Please transfer numbers now.\nOnce you have completed the transfer, press ( Y ) to continue. Press any other button to canncel.").lower()
    if z == 'y':
        list_numbers(space=to_space, auth=encoding(f'{to_project}:{to_token}'), lists=receiving_number_list)
        finalizer(auth=encoding(f'{to_project}:{to_token}'))
    else:
        x = input(
            f"Are you sure you want to cancel? Press ( Y ) to cancel. Press any other button to continue").lower()
        if x != 'y':
            confirmation()


list_numbers(space=from_space, auth=encoding(f'{from_project}:{from_token}'), lists=originating_number_list)

confirmation()
