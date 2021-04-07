import os
import time
import re
import xml.etree.cElementTree as ET
import tempfile
import asyncio
from ppadb.client import Client

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

tempFile = tempfile.gettempdir()


#Validates whether there are devices attached
if (len(devices) == 0):
    print('No devices attached')
    quit()

device = devices[0]


#List of Helper functions
def openApp(targetApp):
    device.shell(f'monkey -p {targetApp} -c android.intent.category.LAUNCHER 1')
    device.shell('sleep 2')
    device.shell('input keyevent 3')
def goHome():
    device.shell('input keyevent 3')
def enter():
    device.shell('input keyevent 66')
def scrollDown(targetRange):
    device.shell(f'input swipe 500 2000 500 {targetRange} 500')
def goBack():
    device.shell('input keyevent 4')

def typetext(text):
    device.shell(f"input text {text}")

def sleep(num):
    device.shell(f"sleep {num}")

def openChrome():
    device.shell('am start -n com.android.chrome/com.google.android.apps.chrome.Main')

def wakeUp():
    device.shell('input keyevent KEYCODE_WAKEUP')
    device.shell('input swipe 500 2000 500 100 200')

def dpadDown(num):
    for i in range(num):
        device.shell('input keyevent 20')

def dpadUp(num):
    for i in range(num):
        device.shell('input keyevent 19')

def dpadRight():
    for i in range(num):
        device.shell('input keyevent 22')

def dpadLeft():
    for i in range(num):
        device.shell('input keyevent 21')

def openSetting():
    device.shell('am start -a android.settings.SETTINGS')

def runUi():
    os.popen(f'adb wait-for-device')
    # Run UI Automator on device and save to destination
    os.popen(f'adb shell uiautomator dump /data/local/tmp/uidump.xml')

    time.sleep(2)
    # Pull the xml file into destination tempFile on PC
    os.popen(f'adb pull /data/local/tmp/uidump.xml {tempFile}')




def openTenApps():
    openApp('com.ebay.mobile')
    openApp('com.facebook.katana')
    openApp('com.netflix.mediaclient')
    openApp('com.instagram.android')
    openApp('com.twitter.android')
    openApp('com.ubercab')
    openApp('com.facebook.orca')
    openApp('com.soundcloud.android')
    openApp('com.pinterest')
    openApp('com.snapchat.android')

# Create a temporary file location on PC

pattern = re.compile(r'\d+')


##I only need to pull the dump file from ONE device. No need to do it on all devices

def tapTarget(targetText, id, xadjust=0, yadjust=0):
    os.popen(f'adb -s {id} wait-for-device')
    # Run UI Automator on device and save to destination
    os.popen(f'adb -s {id} shell uiautomator dump /data/local/tmp/uidump.xml')

    time.sleep(1.5)
    # Pull the xml file into destination tempFile on PC
    os.popen(f'adb -s {id} pull /data/local/tmp/uidump.xml {tempFile}')

    time.sleep(1.5)
    # parse with element tree
    tree = ET.ElementTree(file=tempFile + '\\uidump.xml')

    treeIter = tree.iter(tag='node')

    counter = 0
    for elem in treeIter:
        if targetText in elem.attrib["text"].lower():
            bounds = elem.attrib["bounds"]
            coords = pattern.findall(bounds)
            global xPoint
            global yPoint
            xPoint = (int(coords[2]) - int(coords[0])) / 2.0 + int(coords[0])
            yPoint = (int(coords[3]) - int(coords[1])) / 2.0 + int(coords[1])
            counter += 1

    if counter == 0:
        print('Word not found')
        quit()
    else:
        print(f'{xPoint}, {yPoint}')
        os.popen(f'adb -s {id} shell input tap {xPoint+xadjust} {yPoint+yadjust}')


def tapExactTarget(target, id):
    targetText = re.compile(fr'^{target}$')
    os.popen(f'adb -s {id} wait-for-device')
    # Run UI Automator on device and save to destination
    os.popen(f'adb -s {id} shell uiautomator dump /data/local/tmp/uidump.xml')

    time.sleep(2)
    # Pull the xml file into destination tempFile on PC
    os.popen(f'adb -s {id} pull /data/local/tmp/uidump.xml {tempFile}')

    time.sleep(2)
    # parse with element tree
    tree = ET.ElementTree(file=tempFile + '\\uidump.xml')

    treeIter = tree.iter(tag='node')

    global xPoint
    global yPoint

    counter = 0
    for elem in treeIter:
        if target == 'i agree':
            if re.match('signinconsentNext', elem.attrib['resource-id']):
                bounds = elem.attrib["bounds"]
                coords = pattern.findall(bounds)
                xPoint = (int(coords[2]) - int(coords[0])) / 2.0 + int(coords[0])
                yPoint = (int(coords[3]) - int(coords[1])) / 2.0 + int(coords[1])
                counter += 1
        else:
            if re.match(targetText, elem.attrib["text"].lower()):
                bounds = elem.attrib["bounds"]
                coords = pattern.findall(bounds)
                xPoint = (int(coords[2]) - int(coords[0])) / 2.0 + int(coords[0])
                yPoint = (int(coords[3]) - int(coords[1])) / 2.0 + int(coords[1])
                counter += 1

    if counter == 0:
        print('Word not found')
        quit()
    else:
        print(f'{xPoint}, {yPoint}')
        os.popen(f'adb -s {id} shell input tap {xPoint} {yPoint}')

def swipe(direction):
    if direction.lower() == 'up':
        device.shell('input swipe 500 2000 500 100 300')
    elif direction.lower() == 'right':
        device.shell('input 100 1000 1500 1000 300')
    elif direction.lower() == 'left':
        device.shell('input swipe 1500 1000 100 1000 300')
    else:
        device.shell('input swipe 500 100 500 1500 300')

for device in devices:
    """VERY IMPORTANT TO REMOVE THE \n CHARACTER"""
    deviceId = device.shell('getprop ro.serialno').replace('\n', '')

    # wakeUp()
    # # #Screentimeout, Rotation
    # device.shell('settings put system screen_off_timeout 600000')
    # device.shell('settings put system accelerometer_rotation 0')



    # openSetting()
    # time.sleep(0.5)
    # scrollDown(600)
    # tapTarget('accounts', deviceId)
    # time.sleep(.5)
    # tapTarget('accounts', deviceId)
    # time.sleep(.5)
    # ###SAMSUNG ACCT
    # tapTarget('add account', deviceId)
    # time.sleep(.5)
    # tapTarget('samsung account', deviceId)
    # time.sleep(.5)
    # dpadDown(1)
    # typetext('mqltxautomation1@gmail.com')
    # enter()
    # typetext('Testing@2020')
    # enter()
    #
    # time.sleep(5)
    # tapExactTarget('agree', deviceId)
    # time.sleep(3)
    # tapExactTarget('cancel', deviceId)
    # time.sleep(3)
    # goBack()


    # #####GOOGLE ACCT
    # tapTarget('add account', deviceId)
    # time.sleep(.5)
    # tapTarget('google', deviceId)
    # time.sleep(8)
    # dpadDown(3)
    # typetext('gatelab300')
    # enter()
    # time.sleep(5)
    # typetext('Testing@300')
    # enter()
    # time.sleep(5)
    tapExactTarget('i agree', deviceId)


    ##NEED TO CREATE FUNCTION THAT TAPS ONLY EXACT MATCHES
    # tapTarget('agree', deviceId)



    time.sleep(2)



    # # #Opens the 10 standard Apps
    # openTenApps()

