#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# kdenlive slideshow generator
# 2023 Tobias Philipp
# ksg@philipphome.de
# GPL V3
#
# usage: ksg.py projectfile.kdenlive
# you need a prepared kdenlive project file:
# all images in a timeline with the desired duration
# and transitions
# run the tool with the file as arugmuent and
# then open the created slideshow.kdenlive file in kdenlive
# for rendering or further editing
#
# effectListZoom/effectListMove:
# you can choose which zoom/move effects are used
# or how often if you add them multiple times to the list

import xml.etree.ElementTree as ET
import random
import sys

# corner from/to zomming in/out
# 1 top left
# 2 top center
# 3 top right
# 4 middle left
# 5 middle center
# 6 middle right
# 7 bottom left
# 8 bottom center
# 9 bottom right
effectListZoom = (1, 2, 3, 4, 5, 6, 7, 8, 9)

# 10 top left to right
# 11 middle left to right
# 12 bottom left to right
# 13 top right to left
# 14 middle right to left
# 15 bottom  right to left
effectListMove = (10, 11, 12, 13, 14, 15)

# 10% zooming in or out
zoom = 1.1

if(len(sys.argv) < 2 ):
    print ("kdenlive slideshow generator")
    print ("usage: ksg.py projekt.kdenlive")
    sys.exit()

def makeEffect(inTime, outTime, frameW, frameH, imageW, imageH, orientation):

    #portrait image orientation
    if(orientation > 0):
        startW = imageW * (zoom * 2)
        startH = imageH * (zoom * 2)
        endW = imageW * (zoom * 1.5)
        endH = imageH * (zoom * 1.5)

        startX = (frameW - startW) / 2
        startY = startY = (frameH - startH) / 2
        endX = (frameW - endW) / 2
        endY = 0

        return (inTime, round(startX), round(startY), round(startW), round(startH), outTime, round(endX), round(endY), round(endW), round(endH))

    #landscape image orientation

    #1 zoom in, 2 zoom out, 3 move
    effectType = random.randint(1,3)

    effectDirection = random.choice(effectListZoom)

    match effectType:

        case 1:
            startW = imageW
            startH = imageH
            endW = imageW * zoom
            endH = imageH * zoom

        case 2:
            startW = imageW * zoom
            startH = imageH * zoom
            endW = imageW
            endH = imageH

        case 3:
            startW = imageW * zoom
            startH = imageH * zoom
            endW = imageW * zoom
            endH = imageH * zoom
            effectDirection = random.choice(effectListMove)

    match effectDirection:

        # top left
        case 1:
            startX = 0
            startY = 0
            endX = 0
            endY = 0

        # top center
        case 2:
            startX = (frameW - startW) / 2
            startY = 0
            endX = (frameW - endW) / 2
            endY = 0

        # top right
        case 3:
            startX = frameW - startW
            startY = 0
            endX = frameW - endW
            endY = 0

        #middle left
        case 4:
            startX = 0
            startY = (frameH - startH) / 2
            endX = 0
            endY = (frameH - endH) / 2

        #middle center
        case 5:
            startX = (frameW - startW) / 2
            startY = (frameH - startH) / 2
            endX = (frameW - endW) / 2
            endY = (frameH - endH) / 2

        #middle right
        case 6:
            startX = frameW - startW
            startY = (frameH - startH) / 2
            endX = frameW - endW
            endY = (frameH - endH) / 2

        #bottom left
        case 7:
            startX = 0
            startY = frameH - startH
            endX = 0
            endY = frameH - endH

        #bottom center
        case 8:
            startX = (frameW - startW) / 2
            startY = frameH - startH
            endX = (frameW - endW) / 2
            endY = frameH - endH

        #bottom right
        case 9:
            startX = frameW - startW
            startY = frameH - startH
            endX = frameW - endW
            endY = frameH - endH

        #move top left to right
        case 10:
            startX = 0
            startY = 0
            endX = frameW - endW
            endY = 0

        #move middle left to right
        case 11:
            startX = 0
            startY = (frameH - startH) / 2
            endX = frameW - endW
            endY = (frameH - endH) / 2

        #move bottom left to right
        case 12:
            startX = 0
            startY = frameH - startH
            endX = frameW - endW
            endY = frameH - endH

        #move top right to left
        case 13:
            startX = 0
            startY = frameW - startW
            endX = 0
            endY = 0

        #move middle right to left
        case 14:
            startX = frameW - startW
            startY = (frameH - startH) / 2
            endX = 0
            endY = (frameH - endH) / 2

        #move bottom right to left
        case 15:
            startX = frameW - startW
            startY = frameH - startH
            endX = 0
            endY = frameH - endH

    return (inTime, round(startX), round(startY), round(startW), round(startH), outTime, round(endX), round(endY), round(endW), round(endH))


########### start of main

tree = ET.parse(sys.argv[1])
root = tree.getroot()

#print(tree)
#print(root)
# for child in root:
#     print(child.tag, child.attrib)

# root directory for the kdenlive projekt
rootDir = root.attrib['root']

# video profile directory for the kdenlive projekt
profile = root.find('profile')

# get tearget video dimensions
targetWidth = int(profile.attrib['width'])
targetHeight = int(profile.attrib['height'])

filterCounter = 10

for playlist in root.iterfind('playlist'):

    # skip the main_bin playlist
    if(playlist.get('id') != 'main_bin'):

        for entry in playlist.iterfind('entry'):

            entryIn = entry.get('in')
            entryOut = entry.get('out')

            # find producer element
            producer = root.find("./producer[@id='%s']" % entry.get('producer'))
            if producer is None:
                # entry is not a frame
                continue

            # get data from the producer element
            sourceFile = producer.find("./property/[@name='resource']").text
            sourceWidth = int(producer.find("./property/[@name='meta.media.width']").text)
            sourceHeight = int(producer.find("./property/[@name='meta.media.height']").text)

            # skip entry if it already contains a filter
            if entry.find('filter') is not None:
                print("skipping %s (a filter already exists)" % (sourceFile))
                continue
            else:
                print ("working on %s" % (sourceFile))

            # fill the frame with the image
            hRatio = targetWidth / sourceWidth
            vRatio = targetHeight / sourceHeight

            portrait = 0

            # patrait orientation images
            if(sourceHeight > sourceWidth):

                portrait = 1
                ratio = min(hRatio, vRatio)
                calcWidth = sourceWidth * ratio
                calcHeight = sourceHeight * ratio

            # landscape orientation images
            else:
                ratio = max(hRatio, vRatio)
                calcWidth = sourceWidth * ratio
                calcHeight = sourceHeight * ratio

            # add the filter entries
            filter = ET.SubElement(entry, 'filter', {'id' : str(filterCounter)})
            filterCounter += 1

            rotate_center = ET.SubElement(filter, 'property', {'name' : 'rotate_center'})
            rotate_center.text = '1';

            mlt_service  = ET.SubElement(filter, 'property', {'name' : 'mlt_service'})
            mlt_service.text = 'qtblend';

            kdenlive_id = ET.SubElement(filter, 'property', {'name' : 'kdenlive_id'})
            kdenlive_id.text = 'qtblend';

            effectData = makeEffect(entryIn, entryOut, targetWidth, targetHeight, calcWidth, calcHeight, portrait)

            # add the animation
            rect = ET.SubElement(filter, 'property', {'name' : 'rect'})
            rect.text = "%s=%s %s %s %s 1.000000;%s=%s %s %s %s 1.000000" % effectData;

            rotation = ET.SubElement(filter, 'property', {'name' : 'rotation'})
            rotation.text = "%s=0;%s=0" % (entryIn, entryOut);

            compositing = ET.SubElement(filter, 'property', {'name' : 'compositing'})
            compositing.text = '0';

            distort = ET.SubElement(filter, 'property', {'name' : 'distort'})
            distort.text = '0';

            kdenlive_collapsed = ET.SubElement(filter, 'property', {'name' : 'kdenlive:collapsed'})
            kdenlive_collapsed.text = '0';

with open('slideshow.kdenlive', 'wb') as f:
    tree.write(f, encoding='utf-8', xml_declaration=True)
f.close()

print ("slideshow.kdenlive generated")
