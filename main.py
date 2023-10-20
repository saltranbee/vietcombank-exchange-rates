# -*- coding: utf-8 -*-

import requests
import os
from datetime import datetime as dt
import xml.etree.ElementTree as ET

url = 'https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx'
try:
    r = requests.get(url, allow_redirects=True)
    open('rate.xml', 'wb').write(r.content)
except Exception as e:
    print(e)
    exit()
mytree = ET.parse('rate.xml')
myroot = mytree.getroot()

rates = {}

exrates = list(filter(lambda x: x.tag == 'Exrate', myroot))

for exrate in exrates:
    o = {}
    currency_code = None
    for k in exrate.attrib.keys():
        if k == 'CurrencyCode':
            currency_code = exrate.attrib[k]

        if k in ['Buy', 'Sell', 'Transfer']:
            val = exrate.attrib[k]
            try:
                val = float(val.replace(',', ''))
            except ValueError:
                pass

            o[k] = val if type(val) is float else 0

    if currency_code not in rates.keys():
        rates[currency_code] = {}

    rates[currency_code] = o

headers = "Datetime,Buy,Sell,Transfer"

for k in rates.keys():
    file_path = f"dist/{k}.csv"
    timestamp = str(int(dt.now().timestamp()) * 1000)
    text = ""
    new_rate = ",".join(list(map(lambda x: f'"{x}"', dict(sorted(rates[k].items())).values())))
    if os.path.exists(file_path):
        print(f"file {file_path} exist")
        text = text + "\n" + timestamp + "," + new_rate
    else:
        print(f"file {file_path} not exist")
        text = text + headers + "\n" + timestamp + "," + new_rate
    with open(file_path, mode="a+") as file:
        file.write(text)
