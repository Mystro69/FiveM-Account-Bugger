import os
import json
import subprocess
import requests
import time
import subprocess
import win32gui
import pyautogui
import win32con
import shutil

appdata = os.path.expanduser("~") + "\\AppData\\Local"
paths = []
paths2 = []
currentAccount = 0

with open("config.json", "r") as file:
    config = json.load(file)
print("\nFetched config.json")

for dirpath, dirnames, filenames in os.walk("digitals"):
    for f in dirnames:
        for dirpath2, dirnames2, filenames2 in os.walk("digitals\\" + f):
            temp = []
            for f2 in filenames2:
                temp.insert(1,f2)
            paths.insert(1,temp)
            paths2.insert(1,f)

print("\nFetched " + str(len(paths)) + " Accounts")

title_name = "FiveM® by Cfx.re"

def window_callback(hwnd, extra):
    windows = extra
    text = win32gui.GetWindowText(hwnd)
    if title_name in text:
        windows.append(hwnd)

def wait_for_window(title_name):
    windows = []
    win32gui.EnumWindows(window_callback, windows)
    while not windows:
        time.sleep(1)
        win32gui.EnumWindows(window_callback, windows)
    return windows[0]

def listen(window):
    window2 = win32gui.GetWindowText(window) == "FiveM® by Cfx.re"
    while window2:
        time.sleep(1)
        os.startfile("fivem://connect/"+config["server"]) #You can use "fivem://connect/" protocol if fivem is running you can steal and add to your shitty C# server launcher it if you want
        window2 = win32gui.GetWindowText(window) == "FiveM® by Cfx.re"
    subprocess.Popen("TASKKILL /F /IM FiveM.exe") #Title Changes when you succesfully passed the connecting page (Prevents Waiting game to load all props and server files)

def mainThread(currentAccount):
    for dirpath, dirnames, filenames in os.walk(appdata + "\\DigitalEntitlements"):
        for f in filenames:
            os.remove(appdata + "\\DigitalEntitlements\\" + f)
        print("\nDeleted old login info")

    for y in paths[currentAccount]:
        shutil.copy("digitals\\" + paths2[currentAccount] + "\\" + y, appdata + "\\DigitalEntitlements\\")
    print("\nSuccesfully Logged In : " + paths2[currentAccount])

    message = {
        "avatar_url": "https://avatars.githubusercontent.com/u/83551872?v=4",
        "embeds": [
            {
                "author": {
                    "name": "Account Bugger",
                    "url": "https://github.com/Mystro69/",
                    "icon_url": "https://avatars.githubusercontent.com/u/83551872?v=4"
                },
                "fields": [
                    {
                        "name": "Accounts",
                        "value": len(paths2),
                        "inline": True
                    },
                    {
                        "name": "Logged In",
                        "value": f"{paths2[currentAccount]} ({currentAccount + 1}.)",
                        "inline": True
                    }
                ],
                "color": "15922164",
                "footer": {
                    "text": "https://github.com/Mystro69"
                }
            }
        ]
    }
    response = requests.post(config["webhook"], json=message)

    if response.status_code == 204:
        print("\nSent Webhook message")
    else:
        print("An error occurred while sending the webhook message.")

    subprocess.Popen(["FiveM.exe"]) 
    print("\nExecuted FiveM")

    window = wait_for_window(title_name)
    time.sleep(1)
    os.startfile("fivem://connect/"+config["server"])
    print("joining server")
    listen(window)
    time.sleep(3)
    currentAccount += 1
    if currentAccount < len(paths2):
        mainThread(currentAccount)
    else:
        print("done")

print("Started main thread")
mainThread(currentAccount)
