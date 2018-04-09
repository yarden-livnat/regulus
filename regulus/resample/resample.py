import csv
import numpy as np


def resample(sample_input, regulus, sim_dir=None, sim_in=None, sim_out=None):
    sim_method = regulus['sample_method']

    if sim_dir is None:
        sim_dir = 'temp'
        sim_out = 'new_sample_outputs.csv'
        sim_in = 'new_sample_inputs.csv'

    if sim_method == 'deployment':

        import subprocess

        save_samples(sample_input, (sim_dir + '/' + sim_in))
        subprocess.run(
            ['python', '-m', 'scenario', '-t', 'Transition_scenario.xml', '-o', sim_dir, '-p', (sim_dir + '/' + sim_in),
             '-r', sim_out], check=True)

        with open(sim_dir + '/' + sim_out, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            header = next(reader)
            data = [[float(x) for x in row] for row in reader]

        return data


    elif sim_method == 'test':

        import regulus.resample.testfun as testfun

        new_input = testfun.load_input(sample_input)
        new_data = testfun.generateres(new_input)
        return new_data

    elif 'pnnl' in sim_method.lower():

        from regulus.resample.Predictor import Predictor

        data = np.array(regulus['pts'])
        X = data[:, :-1]
        y = data[:, -1]
        model = Predictor(X, y)
        new_data = model.predict(sample_input)
        return new_data


    elif 'ackley' in sim_method.lower():

        from regulus.resample.ackley import calc_ackley

        out = calc_ackley(sample_input)
        return out


    elif 'hart' in sim_method.lower():

        from regulus.resample.Hartmann import calc_Hartmann

        out = calc_Hartmann(sample_input)
        return out


    elif 'predictor' in sim_method.lower():

        from regulus.resample.model import Predictor

        data = np.array(regulus['pts'])
        X = data[:, :-1]
        y = data[:, -1]
        model = Predictor(X, y)
        new_data = model.predict(sample_input)

        out = []

        for i in range(len(sample_input)):
            y = new_data[i]
            out.append(sample_input[i] + [y])
        return out


    else:
        print("can't resample for " + sim_method)
        # exit(255)
        return []


def save_samples(data, filename):
    with open(filename, 'w', newline='') as f:
        report = csv.writer(f, delimiter=',')
        report.writerows(data)


def resample_cli():
    from pathlib import Path
    import argparse
    import json
    import csv

    p = argparse.ArgumentParser()
    p.add_argument('samplefile', help='new sample csv file]')
    p.add_argument('-r', '--reg', help='regulus.json file')

    p.add_argument('-o', '--out', help='output file')

    p.add_argument('--csv', help='save as csv file')
    p.add_argument('--json', help='save as regulus file')
    p.add_argument('--debug', action='store_true', help='compute with all models')

    ns = p.parse_args()

    with open(ns.reg) as reg:
        regulus = json.load(reg)

    dims = regulus['dims']
    measures = regulus['measures']

    with open(ns.samplefile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        sample_input = [[float(x) for x in row[0:len(dims)]] for row in reader]

    pts = resample(sample_input, regulus)

    header = dims + measures

    if ns.csv:
        with open(ns.out, 'w', newline='') as f:
            report = csv.writer(f, delimiter=',')
            report.writerow(header)
            report.writerows(pts)

    if ns.json:
        regulus['pts'] = regulus['pts'] + pts

        if ns.out is None:

            with open(ns.reg, 'w') as f:
                json.dump(regulus, f, indent=2)
        else:
            with open(ns.out, 'w') as f:
                json.dump(regulus, f, indent=2)


if __name__ == '__main__':
    # pass
    resample_cli()
