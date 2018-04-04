import argparse
import json
from pathlib import Path

from regulus import file as rf


def copy_morse(morse):
    obj = {'params': morse['params'], 'complexes': {}}
    for name, mc in morse['complexes'].items():
        obj['complexes'][name] = {
            'type': mc['type'],
            'params': mc['params'],
            'partitions': len(mc['partitions'])
        }
    return obj


def info():
    p = argparse.ArgumentParser()
    p.add_argument('filename', help='input file')
    p.add_argument('-v', '--ver', action='store_true', help='Show version')
    p.add_argument('-d', '--dims', action='store_true', help='dimensions')
    p.add_argument('-m', '--measures', action='store_true', help='measures')
    p.add_argument('-p', '--params', action='store_true', help='params')

    p.add_argument('-P', '--pp', action='store_true', help='pretty print')
    p.add_argument('-S', '--short', action='store_true', help='pretty print (short)')

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

    if ns.pp:
        print(json.dumps(regulus,indent=2))

    if ns.short:
        short = {}
        for key, value in regulus.items():
            if key == 'pts':
                short['pts'] = len(value)
            elif key == 'morse':
                short['morse'] = copy_morse(value)
            else:
                short[key] = value
        print(json.dumps(short, indent=2))


if __name__ == "__main__":
    info()