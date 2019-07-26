import argparse
from regulus import from_csv, save


def main():
    parser = argparse.ArgumentParser(description='Regulus')
    parser.add_argument('csv_file',  type=str, help='csv input file')
    parser.add_argument('--ndims', '-d', type=int)
    parser.add_argument('--out', '-o', type=str)

    ns = parser.parse_args()
    save(from_csv(ns.filename, ns), ns.out)
