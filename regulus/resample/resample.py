def resample(sample_input, regulus):
    from regulus.resample.resample_factory import Resample

    sim_method = regulus['sample_method']
    sample = Resample.factory(sim_method)
    return sample.create(sample_input, regulus)

#
# def resample(sample_input, regulus):
#     sim_method = regulus['sample_method']
#
#     if sim_method == 'deployment':
#
#         import tempfile
#         import subprocess
#         import shutil
#         import os
#         from pathlib import Path
#
#         # Temporary sim_input file
#         [f, sim_in] = tempfile.mkstemp(suffix='.csv', prefix=None, dir=None, text=False)
#         os.close(f)
#
#         with open(sim_in, 'w', newline='') as f:
#             report = csv.writer(f, delimiter=',')
#             report.writerows(sample_input)
#
#         # Temporary sim_dir file
#         sim_dir = tempfile.mkstemp(suffix=None, prefix=None, dir=None)
#         # Temporary sim_out file
#         sim_out = 'out.csv'
#
#         subprocess.run(
#             ['python', '-m', 'scenario', '-t', 'Transition_scenario.xml', '-o', sim_dir, '-p', sim_in,
#              '-r', sim_out], check=True)
#
#         with open(sim_dir + '/' + sim_out, newline='') as csvfile:
#             reader = csv.reader(csvfile, delimiter=',')
#             header = next(reader)
#             data = [[float(x) for x in row] for row in reader]
#
#         # Remove temp files / dirs
#         Path(sim_in).unlink()
#
#         path = Path(sim_dir)
#         if path.exists():
#             shutil.rmtree(sim_dir)
#
#         return data
#
#     elif sim_method == 'test':
#
#         import regulus.resample.testfun as testfun
#
#         new_input = testfun.load_input(sample_input)
#         new_data = testfun.generateres(new_input)
#         return new_data
#
#
#     elif 'ackley' in sim_method.lower():
#
#         from regulus.resample.ackley import calc_ackley
#
#         out = calc_ackley(sample_input)
#         return out
#
#
#     elif 'hart' in sim_method.lower():
#
#         from regulus.resample.Hartmann import calc_Hartmann
#
#         out = calc_Hartmann(sample_input)
#         return out
#
#
#     elif 'predictor' in sim_method.lower():
#
#         from regulus.resample.model import Predictor
#
#         data = np.array(regulus['pts'])
#         X = data[:, :-1]
#         y = data[:, -1]
#         model = Predictor(X, y)
#         new_data = model.predict(sample_input)
#
#         out = []
#
#         for i in range(len(sample_input)):
#             y = new_data[i]
#             out.append(sample_input[i] + [y])
#         return out
#
#
#     elif 'keras' in sim_method.lower():
#         from pathlib import Path
#         from regulus.resample.neural_net import baseline_model
#
#         filename = Path(regulus['attr']['path'])
#         wdir = filename.parent
#         name = regulus['name']
#         weight_file = wdir / "{}.h5".format(name)
#
#         data = np.array(regulus['pts'])
#         X = data[:, :-1]
#         y = data[:, -1]
#
#         if weight_file.exists():
#             print(str(weight_file))
#             model = baseline_model(X, y, fit=False)
#             model.load_weights(str(weight_file))
#         else:
#
#             [model, loss] = baseline_model(X, y)
#             print(loss)
#             model.save_weights(str(weight_file))
#
#         new_data = model.predict(np.array(sample_input))
#
#         import keras.backend.tensorflow_backend as tfbk
#         tfbk.clear_session()
#         out = []
#
#         for i in range(len(sample_input)):
#             y = new_data[i]
#             out.append(sample_input[i] + y.tolist())
#
#         return out
#
#
#     else:
#         print("can't resample for " + sim_method)
#         # exit(255)
#         return []
