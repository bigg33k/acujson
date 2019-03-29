# acujson

Parse JSON output from RTL_433 and send to Graphite


## How To
I run both from a crontab 

`@reboot /usr/local/bin/rtl_433 -F json:acu.json & 
* * * * * /home/pi/acujson.py`
