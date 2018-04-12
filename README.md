# regulus.py


## Installation (for development)

run `python setup develop` then `pip install -e .`


## CLI
Command line programs

### regulus
creates a regulus json file from a set of points (csv file with header)

`regulus --csv <file.csv> [-d <n>] [-h | --help]`


### info
Provides information about a regulus file

`info [-d] [-m] [-p] <regulus.json> [-h | --help]`

### morse
Computes Morse (ascending or descending) or Morse-Smale complex for one or more of 
the measures in a regulus file

`morse [-t|--type [smale|ascend|descend]] [-m <list of measures>] [-k | --knn <n>] [-b|--beta <n>] [-G|--graph <list of options>] 
[-g|--gradient <name>] [-o|--out <output.json] filename.json` 


### resample
Resample with new sample input csv file for one or more of the measures with the sample_method in a regulus file 

`resample input.csv   [-r | --reg <regulus.json>] [-o|--out <output file] --csv save as csv --json save as regulus.json [-h | --help]`

### model
Compute mathematical models for all partitions for all measures in a regulus file

`model regulus.json  [-s | --spec <spec.json>] [-o|--out <output file] [-h | --help]`

### recompute
Recompute topology in a regulus file based on a spec file of parameters

`recompute spec.json  [-o | --out <output file>] [-d|--dir <regulus file directory>] [-h | --help]`

### refine
Refine topology in a regulus file based on a spec file of new samples

`refine spec.json  [-o | --out <output file>] [-d|--dir <regulus file directory>] [-h | --help]`
