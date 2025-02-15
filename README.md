### File Schema Discovery ###
---
The python scans the input directory for *txt* or *csv* files, discovers their schema and loads it into a pandas dataframe.
A json schema file is created and used to determine where to move the file based on the file schema.
The files are then moved into a new folder based on their scheama. All matching files are placed in the same directory.