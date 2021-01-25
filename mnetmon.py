#!/usr/bin/env python3
# coding: utf-8

import socket
import time
import datetime
import os
import sys
 
LOG_FNAME = "netMon.log"
FILE = os.path.join(os.getcwd(), LOG_FNAME)

# set the target host and port for TCP/socket connection monitoring:
uhost="1.1.1.1"
uport=53
if (len(sys.argv)==3):
    uhost=str(sys.argv[1])
    uport=int(sys.argv[2])

def send_ping_request(host=uhost, port=uport, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
    except OSError as error:
        return False
    else:
        s.close()
        return True

def write_permission_check():
    try:
        with open(FILE, "a") as file:
            pass
    except OSError as error:
        print("Log file creation failed")
        sys.exit()
    finally:
        pass

def calculate_time(start, stop):
    time_difference = stop - start
    seconds = float(str(time_difference.total_seconds()))
    return str(datetime.timedelta(seconds=seconds)).split(".")[0]

def mon_net_connection(ping_freq=3):
    monitor_start_time = datetime.datetime.now()
    motd = " *** Network connection monitoring started at: " + str(monitor_start_time).split(".")[0] + " *** \n Sending ping requests every " + str(ping_freq) + " seconds to the " + uhost +":"+str(uport)
    print(motd)
 
    with open(FILE, "a") as file:
        file.write("\n")
        file.write(motd + "\n")
    while True:
        if send_ping_request():
            time.sleep(ping_freq)
        else:
            down_time = datetime.datetime.now()
            fail_msg = "Service Connection Broken around: " + str(down_time).split(".")[0]
            print(fail_msg)
            with open(FILE, "a") as file:
                file.write(fail_msg + "\n")
                i = 0
            while not send_ping_request():
                time.sleep(1)
                i += 1
                if i >= 3600:
                    i = 0
                    now = datetime.datetime.now()
                    continous_message = "Service Unavailabilty Persistent at: " + str(now).split(".")[0]
                    print(continous_message)
                    with open(FILE, "a") as file:
                        file.write(continous_message + "\n")
            up_time = datetime.datetime.now()
            uptime_message = "Restored Service Connectivity at: " + str(up_time).split(".")[0]
 
            down_time = calculate_time(down_time, up_time)
            _m = "Service Connection was Unavailable for " + down_time + " \n "
 
            print(uptime_message)
            print(_m)            
            with open(FILE, "a") as file:
                file.write(uptime_message + "\n")
                file.write(_m + "\n")

mon_net_connection()
