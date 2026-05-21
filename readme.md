What it is:
A DOOM WAD file parser and automap renderer written in Python. Reads the binary WAD format, parses map geometry, BSP trees, subsectors and segs, and renders them using raylib.
What it does currently:

Parses DOOM 1 WAD format (header, directories, map lumps)
Renders automap with linedefs and segs colored by subsector
BSP tree visualization with bounding boxes (red/green)
Interactive BSP tree traversal with arrow keys
Player position marker

Requirements:

Python 3.x
pyray (pip install raylib)
A legal copy of DOOM.WAD placed in data/

How to run:
pip install raylib
python main.py
Controls:

Left/Right arrows — traverse BSP tree children
Up arrow — go back to parent node

Known issues / current state:

Read-only visualization, no gameplay
Texture rendering not implemented
