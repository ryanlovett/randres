# Grabs users from existing databse
# Should be executed from directory above instance
import sqlite3
import csv

conn = sqlite3.connect('instance/randres.sqlite')
db = conn.cursor()

with open('randres/schema.sql') as f:
    db.executescript(f.read())

addy_list = 'randres/assets/address_sample.csv'
with open(addy_list) as fin: 
    dr = csv.DictReader(fin) 
    for i in dr:
        print(i['number'], i['street'], i['unit'], i['city'], i['region'], i['zipcode']) 
        db.execute("INSERT INTO addy (numb, street, unit, city, region, zip) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (i['number'], i['street'], i['unit'], i['city'], i['region'], i['zipcode']))
    conn.commit()

# Add the school list
schl_list = 'randres/assets/schl_sample.csv'
with open(schl_list) as fin: 
    dr = csv.DictReader(fin) 
    for i in dr:
        print(i['SCHNAM09'], i['LSTREE09'], i['LCITY09'], i['LSTATE09'], i['LZIP09']) 
        db.execute("INSERT INTO schl (name, street, city, state, zip) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (i['SCHNAM09'], i['LSTREE09'], i['LCITY09'], i['LSTATE09'], i['LZIP09']))
    conn.commit()
