import requests
import os
from pprint import pprint

intercom_bearer = os.environ.get('INTERCOM_EXPORTER')
head = {
        "accept": "application/json",
        "Intercom-Version": "2.8",
        "authorization": "Bearer " + intercom_bearer
    }

conv_url = "https://api.intercom.io/conversations"
pages = "?per_page=15"


def next_page(headers, page_url, per_page):
    url = page_url + per_page
    response = requests.get(url, headers=headers).json()
    for key, value in response.items():
        if isinstance(value, dict):
            for k, v in value.items():
                if k == 'next':
                    starting_after = "&starting_after=" + v['starting_after']
                    return page_url + per_page + starting_after


def conversation_details(headers, page_url, conv_id):
    url = page_url + conv_id
    response = requests.get(url, headers=headers)
    pprint(response.text)


def main(headers, page_url, per_page):
    url = page_url + per_page
    response = requests.get(url, headers=headers).json()
    for key, value in response.items():
        if isinstance(value, list):
            for item in value:
                for k, v in item.items():
                    if k == 'id':
                        print(v)
                        # conversation_details(head,page_url, v)

        if isinstance(value, dict):
            for k, v in value.items():
                if k == 'next':
                    starting_after = "&starting_after=" + v['starting_after']
                    print(page_url + per_page + starting_after)


if __name__ == '__main__':
    main()



