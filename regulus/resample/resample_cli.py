from regulus.resample.resample import  resample

def resample_cli():
    import argparse
    import json
    import csv

    p = argparse.ArgumentParser()
    p.add_argument('new_sample', help='new sample csv file]')
    p.add_argument('-r', '--reg', help='regulus.json file', required=True)

    p.add_argument('-o', '--out', help='output file')

    p.add_argument('--csv', help='save as csv file')
    p.add_argument('--json', help='save as regulus file')

    ns = p.parse_args()

    filename = ns.reg

    with open(filename) as reg:
        regulus = json.load(reg)

    dims = regulus['dims']
    measures = regulus['measures']

    with open(ns.new_sample) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        sample_input = [[float(x) for x in row[0:len(dims)]] for row in reader]

    pts = resample(sample_input, regulus)

    header = dims + measures

    if ns.csv:
        out = ns.out if ns.out is not None else ns.new_sample

        with open(out, 'w', newline='') as f:
            report = csv.writer(f, delimiter=',')
            report.writerow(header)
            report.writerows(pts)

    if ns.json:
        regulus['pts'] = regulus['pts'] + pts

        if ns.out is not None:
            filename = ns.out
        with open(filename, 'w') as f:
            json.dump(regulus, f, indent=2)


if __name__ == '__main__':
    # pass
    resample_cli()