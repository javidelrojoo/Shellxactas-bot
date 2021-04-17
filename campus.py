import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pymongo
from datetime import datetime
import os
from statistics import mean

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

def count(date=""):
    if date == "":
        count = 0
        for x in mongocampus.find():
            count += x['times']
        return count
    else:
        date = datetime(date.year, date.month, date.day)
        return mongocampus.find({'date': date})[0]['times']

def plot():
    os.system('cmd /c "manim scene.py -iql"')
    return

def plot_old():
    date = []
    times = []

    for x in mongocampus.find():
        date.append(x['date'])
        times.append(x['times'])

    times_mean = [mean(times[:i]) for i in range(1, len(times))]

    with plt.xkcd():
        plt.style.use('dark_background')
        fig, ax = plt.subplots()
        fig.autofmt_xdate()
        myFmt = mdates.DateFormatter('%Y-%m-%d')
        ax.xaxis.set_major_formatter(myFmt)
        ax.spines['top'].set_color('black')
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.spines['right'].set_color('black')
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
        ax.plot(date[:-1], times[:-1], color='red')
        ax.plot(date[:-1], times_mean, label='Promedio')
        ax.plot(date[:-1], times[:-1], color='red', label='Cant. de caidas')
        plt.title('Historico de caidas del campus', color='black')
        plt.legend(labelcolor='black')
        plt.savefig('campus.png')

def average():
    return mean([i['times'] for i in mongocampus.find({},{'_id':0, 'times':1})])