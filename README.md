# eelecRateCalc
python script to compute costs of PG&amp;E E-ELEC Rate tariff
See tariff documentation here:
https://www.pge.com/tariffs/assets/pdf/tariffbook/ELEC_SCHEDS_E-ELEC.pdf

Example run:
~$ ./pge.py 
csv reader start
[INFO] load completed -- csv reader parsed 8760 records from csv
[INFO] data processing complete.
Total Summer costs: $1314.53
Total Winter costs: $2474.98
Total Summer usage: 1314.5261 kWH
Total Winter usage: $2474.9774 kWH

Total electricity cost: $3789.50 (10.38 per day)
[INFO] end report.

Example data format provided by PG&E web site when logged into a given account.
Electric usage,2023-01-01,02:00,02:59,2.70,kWh,
