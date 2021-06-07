#!/usr/bin/env python3

import csv
import random
import hashlib
import json 
import string
import pymysql.cursors

# IO
file = '/Users/narcodeb/Downloads/ccu_dataset_practitioners.csv'
output = open('csv_to_import.csv', 'w')
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='onthefly',
                             password='onthefly2020',
                             database='onthefly',
                             cursorclass=pymysql.cursors.DictCursor)
    
with open(file, newline='', encoding='utf-8') as csvfile:
    csv = csv.reader(csvfile, delimiter=';')
    for row in csv:
        resp = {}
        resp['22'] = row[0]
        resp['11'] = row[1]
        resp['6'] = row[2]
        resp['2'] = row[3]
        resp['1'] = row[4]        
        rand = random.sample(list(string.ascii_letters + string.digits), 15)
        form_id = ''.join(rand) + hashlib.sha1(json.dumps(resp).encode('utf-8')).hexdigest()   
        
        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `responses` (`form_id`, `branch`, `responses`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (form_id, 'Practitioners and Artists', json.dumps(resp)))
            connection.commit()        
        
        print(row)


