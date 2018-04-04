import argparse

from regulus import file as rf


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-v', '--ver', action='store_true', help='Show version and exit')
    p.add_argument('--csv', help='create from a .csv file')
    p.add_argument('-o', '--out', help='output file')

    p.add_argument('-d', '--dims', default=-1, help='number of dimensions. default is all but the last column')
    ns = p.parse_args()

    if ns.ver:
        ver = '0.1.0' # todo: get it from the right place
        print('regulus {}'.format(ver))
        return

    if ns.csv:
        regulus = rf.from_csv(ns.csv, ns.dims)
        rf.save(regulus, ns.out)


if __name__ == "__main__":
    main()