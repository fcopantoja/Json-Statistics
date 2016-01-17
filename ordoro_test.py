from datetime import datetime
import json
import pytz
import re
import requests


def get_user_data(url):
    response = requests.get(url=url)
    data = json.loads(response.text)

    return data['data']


def process_data(data):
    """ Receives a dictionary with users, each entry contains login_date and email fields
    """
    emails, april_emails = [], []
    unique_emails = set()
    domain_counts = dict()

    # We compile email regex
    rgx = re.compile(r'[\w.-]+@([\w.-]+.\w+)')

    # it's O(n) Complexity where n is the size of users
    for user in data:
        email = user['email']
        login_date = user['login_date']

        if email:
            email = str.strip(email)
            emails.append(email)
            unique_emails.add(email)

            # Check for valid email address
            match = re.match(rgx, email)
            if match:
                domain = match.group(1)

                # it's O(1) Complexity!, the in operator is O(1) for dictionaries and sets
                if domain not in domain_counts:
                    domain_counts[domain] = 1
                else:
                    domain_counts[domain] += 1

            if login_date:
                # Parse login_date to datetime object and use utc timezone
                login_datetime = datetime.strptime(format_date(login_date), "%Y-%m-%dT%H:%M:%S%z")
                utc_datetime = login_datetime.astimezone(tz=pytz.utc)
                if utc_datetime.month == 4:
                    april_emails.append(email)

    # it's O(m) Complexity where m <= n
    domain_counts = {k: v for k, v in domain_counts.items() if v > 1}

    return {
        'april_emails': april_emails,
        'your_email': 'fcopantoja@gmail.com',
        'unique_emails': list(unique_emails),
        'user_domain_counts': domain_counts,
        'your_email': 'fcopantoja@gmail.com'
    }


def format_date(str_date):
    """ Prepare string to be used by datetime.strptime using format "%Y-%m-%dT%H:%M:%S%z"
    :param str_date e.g. 2014-04-17T19:14:29+08:00:
    :return e.g. 2014-04-17T19:14:29+0800:
    """
    str_length = len(str_date)
    return str_date[:-6] + str_date[str_length-6:str_length-3] + str_date[str_length-2:]


if __name__ == '__main__':
    url = 'https://9g9xhayrh5.execute-api.us-west-2.amazonaws.com/test/data'

    user_data = get_user_data(url)
    print('Received data: ', user_data)

    processed_user_data = process_data(user_data)
    processed_user_data = json.dumps(processed_user_data)
    print('Processed data:', processed_user_data)

    r = requests.post(url, data=processed_user_data)
    print('Response:', r.content)
