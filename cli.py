import requests
import json
import datetime
from getpass import getpass

address = "http://127.0.0.1"
port = "5000"

def print_hk():
    url = "http://127.0.0.1:5000/api/housekeepinglog"
    response = requests.request("GET", url, headers={}, data={})
    response_json = json.loads(response.text)
    num_logs = len(response_json["data"]["logs"])
    hk = response_json["data"]["logs"][num_logs-3] # id=1
    #print(hk)
    print("STATUS (as of {}){:>12} mode".format(hk["last_beacon_time"], hk["satellite_mode"].upper()))
    print("{} MCU resets.".format(hk["no_MCU_resets"]))
    print("Battery {:>10}v{:>10} IN{:>10} OUT".format(hk["battery_voltage"], hk["current_in"], hk["current_out"]))
    print("Watchdogs{:>10}{:>9}{:>12}".format(hk["watchdog_1"], hk["watchdog_2"], hk["watchdog_3"]))
    print("Panels{:>12}{:>11}{:>13}\n{:>18}{:>11}{:>13}".format(hk["panel_1_current"], hk["panel_2_current"], hk["panel_3_current"], hk["panel_4_current"], hk["panel_5_current"], hk["panel_6_current"]))
    print("Temps.{:>12}{:>11}{:>13}\n{:>18}{:>11}{:>13}".format(hk["temp_1"], hk["temp_2"], hk["temp_3"], hk["temp_4"], hk["temp_5"], hk["temp_6"]))
    print("Power Chnls. {:>5}{:>11}{:>13}".format("#", "enabled", "current"))
    for channel in hk["channels"]:
        print("{:>18}{:>11}{:>13}".format(channel["channel_no"], channel["enabled"], channel["current"]))


if __name__=='__main__':
    username = None
    token = None # auth token

    logo = (r'''
    _______  __      ___    __  _________       ___
   / ____/ |/ /     /   |  / / /_  __/   |     |__ \
  / __/  |   /_____/ /| | / /   / / / /| |     __/ /
 / /___ /   /_____/ ___ |/ /___/ / / ___ |    / __/
/_____//_/|_|    /_/  |_/_____/_/ /_/  |_|   /____/
---------------------------------------------------
---------------- WELCOME, OPERATOR ----------------
---------------------------------------------------''')
    print(logo)
    print_hk()
    print()

    while (True):
        print("Enter a character to continue:")
        print("[i] Login")
        print("[gc] Get all communication logs")
        print("[hk] Get housekeeping")
        print("[fs] Get flight schedules (login required)")
        print("[lc] Send live command (login required)")
        print("[o] Logout")
        print("[q] Quit")
        print(": ", end='')
        choice = input()

        if choice=="i":
            url = address + ":" + port + "/api/auth/login"
            print("username: ", end='')
            username = input()
            pswd = getpass("password: ")
            payload = {
                "username": username,
                "password": pswd
            }
            data = json.dumps(payload)
            headers = {
              'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=data)
            response_json = json.loads(response.text)
            if response_json["status"]=="success":
                print("Logged in.")
            token = response_json["auth_token"]

        elif choice=="gc": # Get all communication logs
            url = address + ":" + port + "/api/communications"
            payload = {}
            headers= {}
            response = requests.request("GET", url, headers=headers, data = payload)
            print(response.text.encode('utf8'))
            
        elif choice=="o":
            if not token:
                print("You need to log in to do that.")
                continue
            url = address + ":" + port + "/api/auth/logout"
            payload = {}
            headers = {
              'Authorization': 'Bearer '+token,
              'Content-Type': 'application/json'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            print(response.text)

        elif choice=="hk":
            url = address + ":" + port + "/api/housekeepinglog/1"
            payload = {}
            headers= {}

            response = requests.request("GET", url, headers=headers, data=payload)

            print(response.text)

        elif choice=="fs":
            if not token:
                print("You need to log in to do that.")
                continue
            url = address + ":" + port + "/api/flightschedules"
            payload = {}
            headers = {
                'Authorization': 'Bearer '+token,
                'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers, data=payload)

            print(response.text.encode('utf8'))
            print(response.text)
            print(response.headers)

        elif choice=="lc":
            if not token:
                print("You need to log in to do that.")
                continue
            url = address + ":" + port + "/api/communications"

            print("Enter the command to be sent:")
            command = input() # TODO sanitize input (import telecommands and check against them)
            timestamp = datetime.datetime.now().isoformat() # now() returns local time
            payload = {
                'message': command,
                'timestamp': timestamp,
                'sender': username, 
                'receiver': 'comm'
            }
            headers = {
                'Authorization': 'Bearer '+token,
                'Content-Type': 'application/json'
            }
            data = json.dumps(payload)

            response = requests.post(url, headers=headers, data=data)
            print(response.text.encode('utf8'))

        elif choice=="q":
            break
        
        else:
            print("Choice not recognized. Please try again.")
            continue
