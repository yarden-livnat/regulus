from .null_model import NullModel
from sklearn.kernel_ridge import KernelRidge


def inv_ridge(context, node):
    partition = node.data
    if partition.y.size < 2:
        return NullModel()
    model = KernelRidge(alpha=1.0, kernel='rbf')
    model.fit(partition.y.reshape(-1, 1), partition.x)
    return model
