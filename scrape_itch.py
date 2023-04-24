#!/usr/bin/env python
# coding=utf8
""" Scrape Pollenrapporten.se """

# For use in home assistant

import requests
from bs4 import BeautifulSoup
import re
import json

location = 'Forshaga'
# Hämta din närmaste plats från https://pollenrapporten.se/prognoser.4.5dae555f13d5eaab600134.html

url = 'https://pollenrapporten.se/' + location
page = requests.get(url)
soup = BeautifulSoup(page.text, features="lxml")

nivaer = soup.select(".pp_innerWrapper .pp_pollentext_liten")

salg_vide_str = nivaer[0].text
alm_str = nivaer[1].text
al_str = nivaer[2].text
bjork_str = nivaer[3].text
hassel_str = nivaer[4].text


def trans_pollenstring(string):
  # Function that takes string and returns integer
  # låga = 1; låga till måttliga = 2; måttliga = 3;
  # måttliga till höga = 4; höga = 5; höga till mycket höga = 6;
  # mycket höga = 7
    if string == "Låga halter":
        return 1
    elif string == "Låga till måttliga":
        return 2
    elif string == "Måttliga halter":
        return 3
    elif string == "Måttliga till höga":
        return 4
    elif string == "Höga halter":
        return 5
    elif string == "Höga till mycket höga":
        return 6
    elif string == "Mycket höga halter":
        return 7
    else:
        return 0


salg_vide_int = trans_pollenstring(salg_vide_str)
alm_int = trans_pollenstring(alm_str)
al_int = trans_pollenstring(al_str)
bjork_int = trans_pollenstring(bjork_str)
hassel_int = trans_pollenstring(hassel_str)

# Hämta prognos, period och text
normal = soup.select(".normal")

period = normal[5].text
period_datum = re.sub('Prognos.* perioden ', '', period)
prognos = normal[6].text

# Jsonize data
data = {
  'output':
  {
    "location": location,
    "period": period_datum,
    "prognos": prognos,
    "salg_vide": salg_vide_int,
    "alm": alm_int,
    "al": al_int,
    "bjork": bjork_int,
    "hassel": hassel_int
  }
}

json_string = json.dumps(data)

print(json_string)

# vim: set ts=4:sw=4:et:
