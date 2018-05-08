import argparse
import json

import regulus.file as rf
from regulus.update.update_model import update_model


def update_model_cli():
    p = argparse.ArgumentParser()
    p.add_argument('filename', help='regulus .json file]')
    p.add_argument('-o', '--out', help='output file')
    p.add_argument('-s', '--spec', help='update_model spec file')

    p.add_argument('-m', '--measure', help='measure to compute similarity')

    ns = p.parse_args()

    regulus = rf.load(ns.filename)

    if ns.spec is None:
        spec = ns.spec
    else:
        with open(ns.spec) as f:
            spec = json.load(f)
    try:
        update_model(regulus, spec, measure=ns.measure)
        filename = ns.out if ns.out is not None else ns.filename
        rf.save(regulus, filename)

    except Exception as e:
        print(e)
        return 1


if __name__ == "__main__":
    update_model_cli()
