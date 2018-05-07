from pathlib import Path
import argparse
import json

from regulus.update.refine_topo import refine


def refine_topo_cli():
    p = argparse.ArgumentParser()
    p.add_argument('specname', help='new sample spec .json file]')
    p.add_argument('-o', '--out', help='output file')
    p.add_argument('-d', '--dir', help='regulus.json file dir')

    ns = p.parse_args()

    with open(ns.specname) as f:
        spec = json.load(f)

    data_dir = Path(ns.dir) if ns.dir is not None else spec.parent

    return refine(spec, data_dir, ns.out)


if __name__ == '__main__':
    refine_topo_cli()
