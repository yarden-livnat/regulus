import argparse
import json
from pathlib import Path

from regulus import file as rf


def info():
    p = argparse.ArgumentParser()
    p.add_argument('filename', help='input file')
    p.add_argument('-v', '--ver', action='store_true', help='Show version')
    p.add_argument('-d', '--dims', action='store_true', help='dimensions')
    p.add_argument('-m', '--measures', action='store_true', help='measures')
    p.add_argument('-p', '--params', action='store_true', help='params')

    p.add_argument('-o', '--out', help='output file')

    ns = p.parse_args()

    filename = Path(ns.filename)

    if filename.suffix != '.json':
        print('unknown file type')
        exit(255)

    regulus = rf.load(ns.filename)

    if ns.ver:
        print('version {}'.format(regulus['version']))
        return

    if ns.dims:
        print('dims[{}: {}'.format(len(regulus['dims']), regulus['dims']))

    if ns.measures:
        print('measures[{}: {}'.format(len(regulus['measures']), regulus['measures']))

    if ns.params:
        morse = regulus['morse']
        print('global: {}'.format(morse['params']))
        for name, mc in morse['complexes'].items():
            print('{}: type:{} params:{}'.format(name, mc['type'], mc['params']))


if __name__ == "__main__":
    info()