#!/usr/bin/python
import os
import sys
import time
import requests
import json
import pytz
import logging
from datetime import datetime
import Adafruit_DHT as dht


logging.basicConfig(level=logging.DEBUG, filename='temp.log', filemode='a+',
                    format='%(levelname)-3s %(message)s')

name = 'mort-pi-1'
url = os.environ.get('CRYPTO_LOGICAPP_URL')
starttime = time.time()

def get_date_time():
    global epoch_time
    global dt
    global year_month

    epoch_time = int(time.time())
    tz = pytz.timezone('America/Chicago')
    dt = datetime.fromtimestamp(epoch_time, tz)
    year_month = datetime.fromtimestamp(epoch_time).strftime('%Y-%m')
    return(epoch_time,dt,year_month)

def get_data():
    global temp_c
    global temp_f
    global humidity
    
    humidity, temp_c = dht.read_retry(11, 4)
    temp_f = temp_c * 9/5.0 + 32
    return(temp_c,temp_f,humidity)

def post_data(url,temp_c,temp_f,humidity,epoch_time,dt,year_month):
    data = {
        'name': name,
        'temp': temp_c,
        'humidity': humidity,
        'epoch': epoch_time,
        'partition_key': year_month
    }
    res = requests.post(url, data=json.dumps(data), 
                        headers={'Content-Type':'application/json'})
    logging.info('{0} - STATUS: {1} - Temp: {2:0.1f} F  Humidity: {3:0.1f} %'
                .format(dt, res, temp_f, humidity))
    return 'SUCCESS'

def main():

    while True:
        
        get_date_time()
        get_data()
        post_data(url,temp_c,temp_f,humidity,epoch_time,dt,year_month)

        time.sleep(60.0 - ((time.time() - starttime) % 60.0))

    return 'SUCCESS'

if __name__ == '__main__':
    main()