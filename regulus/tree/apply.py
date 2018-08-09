

def apply(root, measure):
    for node in root:
        measure(node)


def apply_items(root, measure):
    for partition in root.items():
        measure(partition)