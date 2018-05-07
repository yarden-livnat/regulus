import argparse
import json

import regulus.file as rf
from regulus.update.update_sim import update_sim


def update_sim_cli():
    p = argparse.ArgumentParser()
    p.add_argument('filename', help='regulus .json file]')
    p.add_argument('-o', '--out', help='output file')
    p.add_argument('-m', '--mod', help='model used to fit each partition')
    p.add_argument('-f', '--fun', help='function used to compute similarity')

    ns = p.parse_args()

    regulus = rf.load(ns.filename)

    try:
        update_sim(regulus, sim=ns.fun, model=ns.mod)
        filename = ns.out if ns.out is not None else ns.filename
        rf.save(regulus, filename)

    except Exception as e:
        print(e)
        return 1


if __name__ == "__main__":
    update_sim_cli()
