# Grabs users from existing databse
# Should be executed from directory above instance
import sqlite3
import csv
import gzip

if str(input("Are you sure you want to run this script? Any existing information in the database will be overwritten (y/n)")).lower() != "y":
    exit()

conn = sqlite3.connect('instance/randres.sqlite')
db = conn.cursor()
conn.text_factory = str

with open('randres/schema.sql') as f:
    db.executescript(f.read())

addy_list = 'randres/assets/address_sample.csv.gz'
with gzip.open(addy_list, mode="rt") as fin: 
    dr = csv.DictReader(fin) 
    for i in dr:
        # print(i['number'], i['street'], i['unit'], i['city'], i['region'], i['zipcode']) 
        db.execute("INSERT INTO addy (numb, street, unit, city, region, zip) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (i['number'], i['street'], i['unit'], i['city'], i['region'], i['zipcode']))
    conn.commit()

# Add the school list
schl_list = 'randres/assets/schl_sample.csv.gz'
with gzip.open(schl_list, mode="rt") as fin: 
    dr = csv.DictReader(fin) 
    for i in dr:
        # print(i['SCHNAM09'], i['LSTREE09'], i['LCITY09'], i['LSTATE09'], i['LZIP09']) 
        db.execute("INSERT INTO schl (name, street, city, state, zip) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (i['SCHNAM09'], i['LSTREE09'], i['LCITY09'], i['LSTATE09'], i['LZIP09']))
    conn.commit()

# Add the ssn list
ssn_list = 'randres/assets/ssn_sample.csv.gz'
with gzip.open(ssn_list, mode="rt") as fin: 
    dr = csv.DictReader(fin) 
    for i in dr:
        db.execute("INSERT INTO ssns (ssn) "
                        "VALUES (?)",
                        (i['ssn'],))
    conn.commit()