#!/usr/bin/python3
''' Read PG&E Hourly kilowatt use CSV file and apply E-ELEC Tariff to generate simulated costs'''
__date__ = 'March 30, 2024'
__author__ = 'mrm@acm.org'
__copyright__ = 'Copyright (C) 2024 Maidhc MacPháidín'
__license__ = 'public domain'

import csv
import re
from datetime import datetime

print("csv reader start")
records = []

rates = { 'winter' : [0.41177, 0.38968, 0.37582],
          'summer' : [0.64328, 0.4814, 0.42472]
          }

with open('pge.csv') as csvfile:
   rdr = csv.reader(csvfile)
   for row in rdr:
       when = "%s %s" % (row[1], row[2])
       at = datetime.strptime(when, '%Y-%m-%d %H:%M')
       amt = row[4]
       records.append((at, amt))

print("[INFO] load completed -- csv reader parsed %s records from csv" % len(records))

summerStart = (6,1)
summerEnd = (9,30)

def setRate(hour):
    ''' return index into rate array: peak(0), halfPeak(1), nonpeak(2) '''
    if hour > 23:
        raise "Invalid value for hour (0-23) got \"%s\"" % (hour)
    # off peak
    if hour < 15:
        return 2
    # peak
    if hour >= 16 and hour < 21:
        return 0
    # half peak
    return 1

# Sum the hours in each category
kilowattHours = {
    'winter': [0.0, 0.0, 0.0],
    'summer': [0.0, 0.0, 0.0]    
}

CostHours = {
    'winter': [0.0, 0.0, 0.0],
    'summer': [0.0, 0.0, 0.0]    
}

lineno = 0

for entry in records:
    when, amt = entry
    lineno += 1
    amt = float(amt)
    try:
       season = "winter" if when.month < 6 or when.month > 9 else "summer"
       rateIndex = setRate(when.hour)
       kilowattHours[season][rateIndex] += amt
       CostHours[season][rateIndex] += amt * rates[season][rateIndex]
    except Exception as err:
       print("ERROR: (%s): failed: %s" % (lineno, str(err)))
       import pdb
       pdb.set_trace()

print("[INFO] data processing complete.")
summerCharges = sum(CostHours['summer'])
winterCharges = sum(CostHours['winter'])
print("Total Summer costs: $%.2f" % summerCharges)
print("Total Winter costs: $%.2f" % winterCharges)

summerUsage = sum(kilowattHours['summer'])
winterUsage = sum(kilowattHours['winter'])
print("Total Summer usage: %.4f kWH" % summerCharges)
print("Total Winter usage: $%.4f kWH" % winterCharges)
print()
totalCharges = summerCharges + winterCharges
print("Total electricity cost: $%.2f (%.2f per day)" % (totalCharges, totalCharges / 365))
print("[INFO] end report.")
      
