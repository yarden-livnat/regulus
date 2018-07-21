import argparse
import json

import regulus.file as rf
from regulus.update.update import update


def update_cli():
    p = argparse.ArgumentParser()
    p.add_argument('filename', help='regulus .json file]')
    p.add_argument('-o', '--out', help='output file')
    p.add_argument('-s', '--spec', help='update_model spec file')

    ns = p.parse_args()

    regulus = rf.load(ns.filename)

    spec = None
    if ns.spec is not None:
        with open(ns.spec) as f:
            spec = json.load(f)
    try:
        update(regulus, spec)
        filename = ns.out if ns.out is not None else ns.filename
        rf.save(regulus, filename)

    except Exception as e:
        print(e)
        return 1


if __name__ == "__main__":
    update_cli()
