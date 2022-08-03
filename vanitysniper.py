from wsgiref import headers
from playsound import playsound as play
from http.client import HTTPSConnection
from urllib.error import HTTPError
import requests
from colorama import Fore
import threading
import random
import os

f = open("proxy.txt", 'r')
http = f.readline()
f.close()
f = open("proxy.txt", 'r')
https = f.readline()
f.close()
#user:pass@ip:port or ip@port
proxyDict = {
    "http": http,
    "https": https,
}
f = open("tokenguild.txt", 'r')
tokenguild = f.readline().split(':')
str.split(":")
f.close()
url1 = 'https://discord.com/api/v9/guilds/'+tokenguild[1]+'/vanity-url'

def sniped():
    with open('tokenguild.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('tokenguild.txt', 'w') as fout:
        fout.writelines(data[1:])
    f.close()

def request():
    if os.stat("tokenguild.txt").st_size == 0:
        print(Fore.RED + "Token file is empty")
        os("pause")
        exit()
    else:
        headers = {'authorization': tokenguild[0]}
        while True:
            try:
                lines = open('vanitys.txt').read().splitlines()
                vanity=random.choice(lines)
                url = ('https://discord.com/api/v9/invites/'+vanity)
                response=requests.get(url, proxies=proxyDict)
                if response.status_code == 200:
                    print(Fore.RED + "\nClaimed Vanity -> " + vanity)
                else:
                    print(Fore.GREEN + "\nUnclaimed Vanity -> " + vanity)
                    requests.patch(url1, json={'code': vanity}, headers=headers, proxies=proxyDict)
                    sniped()
            except requests.exceptions.ConnectionError:
                print(Fore.YELLOW + "\nProxy Error")

threads = []

for i in range(5):
    t = threading.Thread(target=request)
    t.daemon = True
    threads.append(t)

for i in range(5):
    threads[i].start()

for i in range(5):
    threads[i].join()

request()