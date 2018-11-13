#! /usr/bin/env python3
import requests
import json
import MySQLdb
import os
import sys
from datetime import timedelta
from datetime import datetime

from time import sleep

INBOUND = 1
OUTBOUND = 2

def init():
    user = os.environ.get('DB_USER', None)
    database = os.environ.get('DB_NAME', None)
    host = os.environ.get('DB_HOST', 'localhost')
    password = os.environ.get('DB_PASSWORD', None)

    if user is None or database is None or password is None:
        print("No DB conf in Environment settings")
        sys.exit(1)
    
        
    conn = MySQLdb.connect(user=user, password = password, host=host, database=database)
    curr = conn.cursor()

    return conn, curr

    

def main(conn, curr):
    
    base_url = 'https://www.metlink.org.nz/api/v1/{endpoint}/{service}'
    services = ['1', '2', '3', '3a', '7', '12', '12e', '13', '14', '17', '17e', '18', '18e', '19', '19e', '20', '21', '22', '23', '23e', '24', '25', '26', '28', '29', '29e', '30x', '31x', '32x', '33', '34', '35', '36', '36a', '37', '52', '56', '57', '58', '60', '60e', '81', '83', '84', '85x', '91', '110', '111', '112', '113', '114', '115', '120', '121', '130', '145', '150', '154', '160', '170', '200', '201', '202', '203', '204', '206', '210', '220', '226', '230', '236', '250', '251', '260', '261', '262', '264', '280', '281', '291', '300', 'N1', 'N2', 'N22', 'N3', 'N4', 'N5', 'N6', 'N66', 'N8', 'N88', '901', '904', '906', '911', '915', '916', '919', '924', '926', '929', '930', '931', '935', '951', '953', '955']

    ins_str = 'INSERT INTO servicelocations(RecordedAtTime,VehicleRef,ServiceID,HasStarted,DepartureTime,OriginStopID,DestinationStopID,Direction,Bearing,BehindSchedule,VehicleFeature,DelaySeconds,lat,lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    delay = 1
    
    for service in services:
        sleep(delay)
        r = requests.get(base_url.format(service=service, endpoint='ServiceLocation'))
        print(r)
        while r.status_code == 429:
            delay *= 2
            sleep(delay)
            print(delay)
            r = requests.get(base_url.format(service=service, endpoint='ServiceLocation'))
            print(r)
        
        if r.status_code != 200:
            print(r.status_code + ' ' + r.text)
            continue
                
        result = r.json()
        values = []
        for bus in result['Services']:
            direction = 0
            if bus['Direction'] == 'Inbound':
                direction = INBOUND
            elif bus['Direction'] == 'Outbound':
                direction = OUTBOUND

            time_str = bus['RecordedAtTime']
            recordedAtTime = datetime.strptime(time_str[:22] + time_str[23:], '%Y-%m-%dT%H:%M:%S%z')
            time_str = bus['DepartureTime']
            departedAtTime = datetime.strptime(time_str[:22] + time_str[23:], '%Y-%m-%dT%H:%M:%S%z')
            
            values.append((recordedAtTime, bus['VehicleRef'], bus['ServiceID'], bus['HasStarted'], departedAtTime, bus['OriginStopID'], bus['DestinationStopID'], direction, bus['Bearing'], bus['BehindSchedule'], bus['VehicleFeature'], bus['DelaySeconds'], bus['Lat'], bus['Long']))
        curr.executemany(ins_str, values)
        conn.commit()


if __name__ == "__main__":
    conn, curr = init()
    main(conn, curr)
    conn.close()
