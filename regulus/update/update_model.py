from regulus.math.similarity import Similarity
from regulus.math.model import Model

MODELS = ['pca', 'linear']
SIMILARITIES = ['parent', 'sibling']


def update_model(regulus, spec=None, sim=None):
    if spec is None:
        for item in MODELS:
            model = Model.factory(item)
            model.compute(regulus)

        if sim is not False:
            for item in SIMILARITIES:
                sim = Similarity.factory(item)
                sim.compute(regulus)

    else:
        for item in spec['model']:
            model = Model.factory(item)
            model.compute(regulus)

        if sim is not False:
            for item in spec['similarity']:
                sim = Similarity.factory(item)
                sim.compute(regulus)
