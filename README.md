# regulus.py


## Installation (for development)

run `python setup develop` then `pip install -e .`


## CLI
Command line programs

### regulus
creates a regulus json file from a set of points (csv file with header)

`regulus --cvs <file.csv> [-d <n>] [-h | --help]`


### info
Provides information about a regulus file

`info [-d] [-m] [-p] <regulus.json> [-h | --help]`

### morse
Computes Morse (ascending or descending) or Morse-Smale complex for one or more of 
the measures in a regulus file

`morse [-type [smale|ascending|descending]] [-m <list of measures>] [-k | --knn <n>] [-b|--beta <n>] [-g|--graph <list of options>] 
[-G|--gradient <name>] [-o|--out <output.json] filename.json` 