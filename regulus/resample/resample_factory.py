import numpy as np
from pathlib import Path


class Resample(object):

    def factory(type):
        if type == "predictor":
            return Predictor()
        elif type == "keras":
            return Keras()
        elif type == "ackley":
            return Ackley()
        elif type == "hartmann":
            return Hartmann()
        elif type == "test":
            return Test()
        elif type == "deployment":
            return Deployment()
        raise AssertionError("Bad Sampling Method: " + type)

    factory = staticmethod(factory)


class Deployment(Resample):

    def create(self, sample_input, regulus):
        import csv
        import tempfile
        import subprocess
        import shutil
        import os

        # Temporary sim_input file
        [f, sim_in] = tempfile.mkstemp(suffix='.csv', prefix=None, dir=None, text=False)
        os.close(f)

        with open(sim_in, 'w', newline='') as f:
            report = csv.writer(f, delimiter=',')
            report.writerows(sample_input)

        # Temporary sim_dir file
        sim_dir = tempfile.mkstemp(suffix=None, prefix=None, dir=None)
        # Temporary sim_out file
        sim_out = 'out.csv'

        subprocess.run(
            ['python', '-m', 'scenario', '-t', 'Transition_scenario.xml', '-o', sim_dir, '-p', sim_in,
             '-r', sim_out], check=True)

        with open(sim_dir + '/' + sim_out, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            header = next(reader)
            data = [[float(x) for x in row] for row in reader]

        # Remove temp files / dirs
        Path(sim_in).unlink()

        path = Path(sim_dir)
        if path.exists():
            shutil.rmtree(sim_dir)

        return data


class Predictor(Resample):
    def create(self, sample_input, regulus):
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


class Keras(Resample):
    def create(self, sample_input, regulus):

        from regulus.resample.neural_net import baseline_model
        import keras.backend.tensorflow_backend as tfbk

        filename = Path(regulus['attr']['path'])
        wdir = filename.parent
        name = regulus['name']
        weight_file = wdir / "{}.h5".format(name)

        data = np.array(regulus['pts'])
        X = data[:, :-1]
        y = data[:, -1]

        if weight_file.exists():
            print(str(weight_file))
            model = baseline_model(X, y, fit=False)
            model.load_weights(str(weight_file))
        else:

            [model, loss] = baseline_model(X, y)
            print(loss)
            model.save_weights(str(weight_file))

        new_data = model.predict(np.array(sample_input))

        tfbk.clear_session()
        out = []

        for i in range(len(sample_input)):
            y = new_data[i]
            out.append(sample_input[i] + y.tolist())

        return out


class Test(Resample):
    def create(self, sample_input, regulus):
        import regulus.resample.testfun as testfun

        new_input = testfun.load_input(sample_input)
        new_data = testfun.generateres(new_input)
        return new_data


class Ackley(Resample):
    def create(self, sample_input, regulus):
        from regulus.resample.ackley import calc_ackley

        out = calc_ackley(sample_input)

        return out


class Hartmann(Resample):
    def create(self, sample_input, regulus):
        from regulus.resample.Hartmann import calc_Hartmann

        out = calc_Hartmann(sample_input)
        return out
