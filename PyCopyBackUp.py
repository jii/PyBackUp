# -*- coding: utf-8 -*-
# zalohovaci software by jii 23.09.2020
#http://sys.ostroh.cz/backupadd/?cmd=cmd test&log=log test&pc=pc test
# jméno PC nesmí mít mezeru
# https://www.geeksforgeeks.org/working-zip-files-python/
# přidej zipovaní
import os, shutil, sys

from datetime import datetime
import urllib.request 
    
path = "backupFolder"
moveto = "//ip/zalohaPohoda/zalohaSklad/"

from contextlib import contextmanager

@contextmanager
def network_share_auth(share, username=None, password=None, drive_letter='P'):
    """Context manager that mounts the given share using the given
    username and password to the given drive letter when entering
    the context and unmounts it when exiting."""
    cmd_parts = ["NET USE %s: %s" % (drive_letter, share)]
    if password:
        cmd_parts.append(password)
    if username:
        cmd_parts.append("/USER:%s" % username)
    os.system(" ".join(cmd_parts))
    try:
        yield
    finally:
        os.system("NET USE %s: /DELETE" % drive_letter)


if datetime.today().strftime('%A') == "Monday":
    dnes = "pondeli"
if datetime.today().strftime('%A') == "Tuesday":
    dnes = "utery"
if datetime.today().strftime('%A') == "Wednesday":
    dnes = "streda"
if datetime.today().strftime('%A') == "Thursday":
    dnes = "ctvrtek"
if datetime.today().strftime('%A') == "Friday":
    dnes = "patek"
if datetime.today().strftime('%A') == "Saturday":
    sys.exit()
if datetime.today().strftime('%A') == "Sunday":
    sys.exit()
moveto = moveto + dnes+"/"
files = os.listdir(path)
files.sort()
fx = open("BackUp.log", "a")
now = datetime.now()
fx.write("Run  "+ now.strftime("%H:%M:%S - %m/%d/%y") +"\n")
urllib.request.urlopen("http://ip/backupadd/?cmd=Run&log=Spusteni&pc=ServerPohodaSklad")
for f in files:
    src = path+f
    dst = moveto+f
    with network_share_auth(r"\\server\folder", "login", "pass"):
        shutil.move(src,dst)
    fx.write("Presunoto "+src+" do "+dst+" v "+ now.strftime("%H:%M:%S - %m/%d/%y") +"\n")

    print("Presunoto "+src+" do "+dst+" v "+now.strftime("%H:%M:%S - %m/%d/%y"))
    url = "http://ip/backupadd/?cmd="+dst.replace(' ', '_')+"&log=Presun&pc=ServerPohodaSklad"
    print(url)
    urllib.request.urlopen(url)
fx.write("Konec "+ now.strftime("%H:%M:%S - %m/%d/%y") +"\n")
urllib.request.urlopen("http://ip/backupadd/?cmd=End&log=Konec&pc=ServerPohodaSklad")
fx.close()