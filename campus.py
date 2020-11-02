import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pymongo
import os

mongo_url = os.getenv('MONGO_URL')
mongoclient = pymongo.MongoClient(mongo_url)
mongoprueba = mongoclient['Shellxactas']
mongocampus = mongoprueba['campus']


def estado_campus(timeout):
    try:
        r = requests.get('https://campus.exactas.uba.ar/', timeout=timeout)
    except requests.exceptions.ConnectTimeout:
        return False
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
    except requests.exceptions.ConnectTimeout:
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


def plot():
    date = []
    times = []

    for x in mongocampus.find():
        date.append(x['date'])
        times.append(x['times'])

    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    myFmt = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(myFmt)
    ax.plot(date[:-1], times[:-1])
    plt.title('Historico de caidas del campus')
    plt.savefig('campus.png')
