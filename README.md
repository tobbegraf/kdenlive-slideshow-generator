# kdenlive slideshow generator
2023 Tobias Philipp\
ksg@philipphome.de\
GPL V3

This tool will take a existing Kdenlive project files with picures in the timeline
and will add zomm and move effects to every picture.
The output will be stored in the file slideshow.kdenlive in the working directory.

usage: ksg.py projectfile.kdenlive

You need a prepared kdenlive project file:
All images in a timeline with the desired duration
and transitions.
Run the tool with the filename as arugmuent and
then open the created slideshow.kdenlive file in kdenlive
for rendering or further editing.
