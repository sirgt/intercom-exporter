import requests
import os
import json

intercom_bearer = os.environ.get('INTERCOM_EXPORTER')

head = {
        "accept": "application/json",
        "Intercom-Version": "2.8",
        "authorization": "Bearer " + intercom_bearer
    }

conv_url = "https://api.intercom.io/conversations"
pages = "?per_page=150"


def conversation_details(headers, page_url, conv_id):
    url = page_url + "/" + conv_id
    file_name = os.path.join("./conversations/", conv_id+".json")
    if os.path.isfile(file_name):
        print("Conversation " + file_name + " exists.")
    else:
        response = requests.get(url, headers=headers).json()
        with open(file_name, "w") as outfile:
            json.dump(response, outfile)


def main(headers, page_url, per_page):
    url = page_url + per_page
    response = requests.get(url, headers=headers).json()

    for key, value in response.items():
        if isinstance(value, dict):
            for k, v in value.items():
                if k == 'total_pages':
                    total_pages = v

    for i in range(total_pages):
        print(url)
        response = requests.get(url, headers=headers).json()

        for key, value in response.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    if k == 'next':
                        starting_after = \
                            "&starting_after=" + v['starting_after']
                        url = page_url + per_page + starting_after

            if isinstance(value, list):
                for item in value:
                    for k, v in item.items():
                        if k == 'id':
                            print(v)
                            conversation_details(head, page_url, v)


if __name__ == '__main__':
    main(head, conv_url, pages)

