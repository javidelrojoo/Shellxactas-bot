import requests


def estado_campus(timeout):
    try:
        r = requests.get('https://campus.exactas.uba.ar/', timeout=timeout)
    except requests.exceptions.ReadTimeout:
        return False
    statuscode = str(r.status_code)
    if statuscode.startswith('4') or statuscode.startswith('5'):
        return False
    if statuscode.startswith('2'):
        return True


def ping(timeout, url):
    if not url.startswith('https://'):
        url = 'https://' + url
    try:
        r = requests.get(url, timeout=timeout)
    except requests.exceptions.ReadTimeout:
        return 0
    except requests.exceptions.ConnectionError:
        return 2
    except requests.exceptions.InvalidURL:
        return 3
    statuscode = str(r.status_code)
    if statuscode.startswith('4') or statuscode.startswith('5'):
        return 0
    if statuscode.startswith('2'):
        return 1
