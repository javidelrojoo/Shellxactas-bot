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
