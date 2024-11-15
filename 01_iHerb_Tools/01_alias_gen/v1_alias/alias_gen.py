import os
import json
import requests
import time
import collections
import io

from collections import defaultdict

bot = 'bots'
id = 'id'
botName = 'botName'
status = 'status'
isLifted = 'isLifted'
podName = 'podName'
chargerLevel = 'chargeLevel'
chargerId = 'chargerId'
location = 'location'
path = 'path'
dateUpdated = 'dateUpdated'
isPaused = 'isPaused'
botIp = 'botIp'
taskStatus = 'taskStatus'

bot_list = []
bot_ip_list = []
bot_new_list = []

cmd_seq = {}

connect_err = 0

if __name__ == "__main__":

    f = open(os.getcwd() + '\\config.json', 'r')
    config = json.load(f)
    f.close()

    url_elgin = config["bot_live_elgin"]
    url_atlanta = config["bot_live_atlanta"]
    cmd = config["cmd"]

    while True:
        try:
            elgin_r = requests.get(url_elgin)
        except:
            connect_err += 1
            print(f"!!!Connection Error!!! Retrying ... <{connect_err:.>5}>")
            time.sleep(1)
            continue
        else:
            break
    try:
        elgin_json = elgin_r.json() # Return a dictionary
        for robot in elgin_json[bot]:
            bot_list.append(int(robot[botName]))
            bot_ip_list.append(robot[botIp])
    except Exception as e:
        print(e)

    # for bot in range(110, )


    while True:
        try:
            atlanta_r = requests.get(url_atlanta)
        except:
            connect_err += 1
            print(f"!!!Connection Error!!! Retrying ... <{connect_err:.>5}>")
            time.sleep(1)
            continue
        else:
            break
    try:
        atlanta_json = atlanta_r.json() # Return a dictionary\
        for robot in atlanta_json[bot]:
            bot_list.append(int(robot[botName]))
            bot_ip_list.append(robot[botIp])
    except:
        print("AGA json error")
    # for bot in range(110, 555):
    #     bot_list.append(bot)

    d = defaultdict(lambda: 0)

    temp_list = []
    # Base
    base_bot = "alias {}{}=\"ssh -o StrictHostKeyChecking=no root@{} '{}'\""
    for index in range(len(bot_list)):
        for command in cmd.values():
            temp_list.append(base_bot.format(command[0], bot_list[index], bot_ip_list[index], command[1]))
        tunnel = "alias tnl_e" + str(bot_list[index]) + "=\"ssh -o StrictHostKeyChecking=no -L 15000:192.168.75.2:5000 root@" + str(bot_ip_list[index]) + "\""
        temp_list.append(tunnel)
        d[bot_list[index]] = temp_list
        temp_list = []

# ssh -o StrictHostKeyChecking=no -L root@172.17.34.152 15000:192.168.75.2:5000
    fp = io.open('py_alias.sh', 'w', newline='\n')
    od = collections.OrderedDict(sorted(d.items()))
    # print(od)
    for index in od.items():
        for cmd in index[1]:
            fp.write(cmd)
            fp.write('\n')
        fp.write('\n')
    fp.close()
