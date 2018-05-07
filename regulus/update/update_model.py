from regulus.math.model import Model

MODELS = ['pca', 'linear']


def update_model(regulus, spec=None):
    if spec is None:
        for item in MODELS:
            model = Model.factory(item)
            model.compute(regulus)

    else:
        for item in spec['model']:
            model = Model.factory(item)
            model.compute(regulus)
