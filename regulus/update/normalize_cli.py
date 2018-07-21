import argparse

from regulus import file as rf
from regulus.update.normalize import normalize


def normalize_cli():
    p = argparse.ArgumentParser()
    p.add_argument('filename', help='regulus .json file]')
    p.add_argument('-o', '--out', help='output file')

    ns = p.parse_args()

    regulus = rf.load(ns.filename)
    normalize(regulus)
    rf.save(regulus, ns.out)


if __name__ == "__main__":
    normalize_cli()