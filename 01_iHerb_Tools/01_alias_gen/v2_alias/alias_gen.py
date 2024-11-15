import os
import json
import sys
import requests
import collections
import io

from colorama import init, Fore
from collections import defaultdict

BOT = 'bots'
NAME = 'botName'
IP = 'botIp'

TIMEOUT_DEF = 15

# Init
init(autoreset = True)

# Get path
if getattr(sys, 'frozen', False):
    path = os.path.dirname(sys.executable)
elif __file__:
    path = os.path.abspath(os.path.dirname(__file__))

# Load config data
f = open(path + '\\config.json', 'r')
config = json.load(f)
f.close()

# Warehouse bot url list
warehouse_url_list = config['warehouse_url']
# Cmd list
cmd_list = config['cmd']

d = defaultdict(lambda: 0)
base_pattern = "alias {}{}=\"ssh -o StrictHostKeyChecking=no root@{} '{}'\""

# Parse
for url in warehouse_url_list:
    try:
        # Get data
        rq = requests.get(url, timeout = TIMEOUT_DEF)
        # Convert to dict
        bot_live_data = rq.json()
        # bot_live_data = {"bots":[{k:v, k1:v1, ...}, {kn:vn, ...}, {km:vm, ...}, ...]}
        temp_list = []
        for index in range(len(list(bot_live_data.values())[0])):
            bot_name = str(bot_live_data[BOT][index][NAME])
            bot_ip = str(bot_live_data[BOT][index][IP])
            for cmd in cmd_list:
                # Create cmd for each bot
                temp_list.append(base_pattern.format(cmd[0], bot_name, bot_ip, cmd[1]))
                # Tunnel for a bot, use when capture camera's picture
                tunnel = "alias tnl_e" + bot_name + "=\"ssh -o StrictHostKeyChecking=no -L 15000:192.168.75.2:5000 root@" + bot_ip + "\""
            temp_list.append(tunnel)
            # Append to dict d = {"bot_name":"cmd", ...}
            d[bot_name] = temp_list
            temp_list = []
    except requests.exceptions.ConnectTimeout as e:
        print(Fore.GREEN + str(e))
        os._exit(-1)
    except Exception as e:
        print(Fore.RED + str(e))
        os._exit(-1)

fp = io.open(path + '\\py_alias.sh', 'w', newline='\n')
# Sort data as bot name (str)
od = collections.OrderedDict(sorted(d.items()))
for index in od.values():
    for cmd in index:
        fp.write(cmd)
        fp.write('\n')
    fp.write('\n')
fp.close()
