import tempfile
import os
import re
import time
import xml.etree.cElementTree as ET

#Creates a new temporary file location to store the XML file pulled from device
tempFile = tempfile.gettempdir()

#Generates dumpfile and pulls from device onto tempFile location
os.popen('adb shell uiautomator dump /data/local/tmp/uidump.xml')
os.popen(f'adb pull /data/local/tmp/uidump.xml {tempFile}')


#creates an element tree using the pulled XML file
tree = ET.ElementTree(file = tempFile + '\\uidump.xml')

#using recursive method to pull out all iterations with the "node" tags
treeIter = tree.iter(tag="node")

#defining the pattern to look for when going through all the tree elements
coordPattern = re.compile(r'\d+')

#defining the target that the element needs to CONTAIN in order to satisfy the coordinate search
target = 'Face recognition'

#iterating through the elements to find if TARGET is included in the element attribute with 'text'
#if found - the bounds are grabbed by using regex method and then split into x point and y point.
for e in treeIter:
    if target in e.attrib["text"]:
        bounds = e.attrib["bounds"]
        coords = coordPattern.findall(bounds)
        xPoint = (int(coords[2]) - int(coords[0])) / 2.0 + int(coords[0])
        yPoint = (int(coords[3]) - int(coords[1])) / 2.0 + int(coords[1])

#this is to make sure that the program is running and grabbing the coordinates. User can not use 'adb shell input tap x y' command to select the target element
print(xPoint, yPoint)
