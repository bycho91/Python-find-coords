import tempfile
import os
import re
import time
import xml.etree.cElementTree as ET

tempFile = tempfile.gettempdir()


os.popen('adb shell uiautomator dump /data/local/tmp/uidump.xml')
os.popen(f'adb pull /data/local/tmp/uidump.xml {tempFile}')

tree = ET.ElementTree(file = tempFile + '\\uidump.xml')

treeIter = tree.iter(tag="node")

coordPattern = re.compile(r'\d+')

target = 'Face recognition'

for e in treeIter:
    if target in e.attrib["text"]:
        bounds = e.attrib["bounds"]
        coords = coordPattern.findall(bounds)
        xPoint = (int(coords[2]) - int(coords[0])) / 2.0 + int(coords[0])
        yPoint = (int(coords[3]) - int(coords[1])) / 2.0 + int(coords[1])

print(xPoint, yPoint)
