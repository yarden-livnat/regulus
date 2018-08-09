
from regulus.errors.error import RegulusMissingError
from regulus.models.linear_model import MODEL_NAME


FITNESS_NAME = 'parent_fitness'


def parent_fitness(node):
    partition = node.data
    if node.parent is None:
        partition.attr[FITNESS_NAME] = 1
    else:
        parent = node.parent.data
        if MODEL_NAME in parent.models:
            partition.attr[FITNESS_NAME] = parent.models[MODEL_NAME].score(partition.x, partition.y)
        else:
            raise RegulusMissingError("Model {} not found in partition {}".format(MODEL_NAME, parent.id))
