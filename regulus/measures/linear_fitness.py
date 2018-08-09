from regulus.models.linear_model import MODEL_NAME
from regulus.errors.error import RegulusMissingError

FITNESS_NAME = 'linear_fitness'


def linear_fitness(node):
    partition = node.data
    if MODEL_NAME in partition.models:
        partition.attr[FITNESS_NAME] = partition.models[MODEL_NAME].score(partition.x, partition.y)
    else:
        raise RegulusMissingError("Model {} not found in partition {}".format(MODEL_NAME, partition.id))

