from collections import deque
from heapq import heappush, heappop


class Visited(object):
    def __init__(self, node):
        self.visited = node


def traverse(root,  **kwargs):
    return depth_first(root, **kwargs)


def breath_first(root, post=False, both=False, **kwargs):
    if post or both:
        return breath_first_post(root, both=both, **kwargs)
    return breath_first_pre(root, **kwargs)


def breath_first_pre(root, is_leaf=lambda n: n.is_leaf()):
    queue = deque([root])
    while queue:
        node = queue.popleft()
        yield node
        if not is_leaf(node):
            queue.extend(node.children)


def breath_first_post(root, is_leaf= lambda n: n.is_leaf(), both=False):
    queue = deque([None, root])
    order = []
    while queue:
        node = queue.popleft()
        if node is None:
            # end of level. save nodes at this level in reverse order
            if queue:
                order.extend(reversed(queue))
                queue.append(None)
            continue
        if both:
            yield node
        if not is_leaf(node):
            queue.extend(node.children)
    while order:
        yield order.pop()


def depth_first(root, is_leaf=lambda n: n.is_leaf(), post=False, both=False):
    pre = both or not post
    queue = deque()
    queue.append(root)
    while queue:
        node = queue.pop()
        if isinstance(node, Visited):
            yield node.visited
        else:
            if pre:
                yield node
            if post:
                queue.append(Visited(node))
            if not is_leaf(node):
                queue.extend(reversed(node.children))


def best_first(root, value, is_leaf=lambda n: n.is_leaf()):
    heap = []
    for node in depth_first(root, is_leaf):
        heappush(heap, [value(node), node])
    while heap:
        item = heappop(heap)
        yield item
