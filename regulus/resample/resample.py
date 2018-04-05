import subprocess
import csv
import numpy as np

import testfun
from Predictor import Predictor
from ackley import calc_ackley
from Hartmann import calc_Hartmann


def resample(sample_input, regulus, sim_dir, sim_in, sim_out):
    sim_method = regulus['sim_method']
    if sim_method == 'deployment':
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
        new_input = testfun.load_input(sample_input)
        new_data = testfun.generateres(new_input)
        return new_data

    elif 'pnnl' in sim_method.lower():
        data = np.array(regulus['pts'])
        X = data[:, :-1]
        y = data[:, -1]
        model = Predictor(X, y)
        new_data = model.predict(sample_input)
        return new_data


    elif 'ackley' in sim_method.lower():
        out = calc_ackley(sample_input)
        return out


    elif 'hart' in sim_method.lower():
        out = calc_Hartmann(sample_input)
        return out


    else:
        print("can't resample for " + sim_method)
        # exit(255)
        return []


def save_samples(data, filename):
    with open(filename, 'w', newline='') as f:
        report = csv.writer(f, delimiter=',')
        report.writerows(data)
