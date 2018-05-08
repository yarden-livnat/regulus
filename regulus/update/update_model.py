from regulus.math.model import create_models


def update_model(regulus, spec=None, measure=None):
    # if spec is None:
    #    for item in MODELS:
    #        model = Model.factory(item)
    #        model.compute(regulus)
    #
    # else:
    #    for item in spec['model']:
    #        model = Model.factory(item)
    #        model.compute(regulus)
    create_models(regulus, spec, measure)
