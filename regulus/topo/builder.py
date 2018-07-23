from collections import defaultdict
from regulus.topo.topology import Partition, Node


class Merge(object):
    def __init__(self, level, is_max, src, dest):
        self.level = level
        self.is_max = is_max
        self.src = src
        self.dest = dest


class PartitionNode(object):
    _id_generator = -1

    @staticmethod
    def gen_id():
        PartitionNode._id_generator += 1
        return PartitionNode._id_generator

    @staticmethod
    def reset():
        PartitionNode._id_generator = -1

    def __init__(self, persistence, base_pts=None, min_idx=None, max_idx=None, child=None, is_max=None):
        self.id = PartitionNode.gen_id()
        self.persistence = persistence
        self.span = []
        self.parent = None
        self.children = []

        self.extrema = []
        self.base_pts = base_pts if base_pts is not None else []
        self.min_idx = min_idx
        self.max_idx = max_idx
        self.max_merge = is_max

        if child is not None:
            self.min_idx = child.min_idx
            self.max_idx = child.max_idx
            self.children.append(child)
            child.parent = self

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        if child.min_idx != self.min_idx and child.max_idx != self.max_idx:
            print("ERROR: child {} [{} {}] merged into parent {} [{} {}] without a matching extrema".format(child.id,
                                                    child.min_idx, child.max_idx, self.id, self.min_idx, self.max_idx))


class Builder(object):
    def __init__(self, debug=False):
        self.base = None
        self.merges = []
        self.min_map = defaultdict(set)
        self.max_map = defaultdict(set)
        self.active = set()
        self.root = None
        self.pts = []
        self.original_pts = set()
        self.debug = debug
        self.mapping = dict()
        self.unique = set()
        self.all = dict()
        self.data_pts = []
        self.single = 0

    def data(self, pts):
        self.data_pts = pts
        return self

    def msc(self, base, hierarchy):
        self.base = base
        for entry in hierarchy:
            row = entry.split(',')
            self.merges.append(Merge(float(row[1]), row[0] == 'Maxima', int(row[2]), int(row[3])))
        return self

    def build(self):
        self.prepare()
        for merge in self.merges:
            # print(merge.level, merge.is_max, merge.src, merge.dest)
            if merge.src == merge.dest:
                continue

            # merge.dest may have been merged already (same persistence level: degenerate case)
            # dest = merge.dest
            # while dest in self.mapping:
            #     dest = self.mapping[dest]
            dest = self.current(merge.dest)
            src = self.current(merge.src)

            if src == dest:
                print('*** loop: dest points back to src', self.find_loop(dest))
                continue

            merge.dest = dest
            merge.src = src
            self.mapping[merge.src] = merge.dest

            if merge.is_max:
                self.update(merge, self.max_map, lambda item: item.min_idx)
            else:
                self.update(merge, self.min_map, lambda item: item.max_idx)

        # get root
        if len(self.active) != 1:
            raise RuntimeError('Error: found {} roots'.format(len(self.active)))
        self.root = self.active.pop()

        self.single = 0
        self.build_idx(self.root, 0)
        print('found {} singles'.format(self.single))

        self.pts.extend([self.root.min_idx, self.root.max_idx])
        self.rename(self.root, 0)
        return self



    # internal

    def prepare(self):
        PartitionNode.reset()
        for key, value in self.base.items():
            m, x = [int(s) for s in key.split(',')]
            p = PartitionNode(0, list(value), m, x)
            self.add(p)

        self.remove_non_unique()

        self.merges.sort(key=lambda m: (m.level, m.src))
        high = self.merges[-1].level
        for merge in self.merges:
            merge.level /= high

        if self.debug:
            for partition in self.active:
                self.check_partition(partition)

    def update(self, merge, idx_map, idx):
        add = []
        remove = set()

        for d in idx_map[merge.dest]:
            n = None
            remove_src = set()
            for s in idx_map[merge.src]:
                if idx(s) == idx(d):
                    if s.persistence == merge.level:
                        # s is an intermediate and should be absorbed
                        if len(s.children) == 0:
                            # s is a base partition
                            d.base_pts.extend(s.base_pts)
                        else:
                            for child in s.children:
                                d.add_child(child)
                    else:
                        if n is None:
                            n = PartitionNode(merge.level, child=d, is_max=merge.is_max)
                            remove.add(d)  # can't be removed during the iterations
                            add.append(n)
                        n.add_child(s)
                    remove_src.add(s)  # can't be removed during the iterations
            for s in remove_src:
                self.remove(s)

        for s in idx_map[merge.src]:
            n = PartitionNode(merge.level, child=s)
            if merge.is_max:
                n.max_idx = merge.dest
            else:
                n.min_idx = merge.dest
            add.append(n)

        for r in remove | idx_map[merge.src]:
            self.remove(r)

        # assign the eliminated extrema as an extra internal point to the first new partition
        if merge.src not in self.unique:
            if len(add) > 0:
                target = add[0]
            else:
                target = next(iter(idx_map[merge.dest]))
            target.extrema.append(merge.src)

        for n in add:
            self.add(n)

    # consistency checks

    def check_partition(self, p):
        min_v = self.data_pts[p.min_idx]
        max_v = self.data_pts[p.max_idx]
        if min_v > max_v:
            print('*** min > max', min_v, max_v)
        for pt_idx in p.base_pts:
            if self.data_pts[pt_idx] < min_v:
                print('*** Partition id:{} min:{} at {} found min:{} at {}'.format(p.id, min_v, p.min_idx, self.data_pts[pt_idx], pt_idx))
            if self.data_pts[pt_idx] > max_v:
                print('*** Partition id:{} max:{} at {} found max:{} at {}'.format(p.id, max_v, p.max_idx, self.data_pts[pt_idx], pt_idx))

    #
    # helpers
    #

    def current(self, partition):
        while partition in self.mapping:
            partition = self.mapping[partition]
        return partition

    def find_loop(self, dest):
        loop = [dest]
        while dest in self.mapping:
            dest = self.mapping[dest]
            loop.append(dest)
        return loop

    def find_unique(self):
        count = defaultdict(int)
        for p in self.active:
            count[p.min_idx] += 1
            count[p.max_idx] += 1
        self.unique = {k for k, v in count.items() if v == 1}
        print('   unique:', self.unique)
        self.all = count

    def remove_non_unique(self):
        for p in self.active:
            for idx in [p.min_idx, p.max_idx]:
                if idx not in self.unique:
                    p.base_pts.remove(idx)

    def add(self, n):
        self.min_map[n.min_idx].add(n)
        self.max_map[n.max_idx].add(n)
        self.active.add(n)

    def remove(self, p):
        self.max_map[p.max_idx].discard(p)
        self.min_map[p.min_idx].discard(p)
        self.active.remove(p)

    def build_idx(self, partition, idx):
        first = idx
        if len(partition.children) == 0:
            if partition.min_idx in partition.base_pts and partition.min_idx not in self.unique:
                print('*** WARNING: min_idx {} in partition {}'.format(partition.min_idx, partition.id))
            if partition.max_idx in partition.base_pts and partition.max_idx not in self.unique:
                print('*** WARNING: max_idx {} in partition {}'.format(partition.max_idx, partition.id))

            n = len(partition.base_pts)
            if n > 0:
                self.pts.extend(partition.base_pts)
                idx += n
        else:
            if len(partition.children) == 1:
                self.single += 1

            if len(partition.extrema) > 0:
                self.pts.extend(partition.extrema)
                idx += len(partition.extrema)

            for child in partition.children:
                idx = self.build_idx(child, idx)

        partition.span = (first, idx)
        return idx

    def rename(self, node, idx):
        node.id = idx
        idx += 1
        if node.persistence > 0:
            for child in node.children:
                idx = self.rename(child, idx)
        return idx

    #
    # save
    #

    def visit(self, p, visitor):
        visitor(p)
        for child in p.children:
            self.visit(child, visitor)

    def tree(self):
        def visit(p, parent):
            partition = Partition(p.id, p.persistence, p.span, [p.min_idx, p.max_idx], p.max_merge)
            node = Node(partition)
            node.parent = parent
            node.children = [visit(child, node) for child in p.children]
            return node

        return visit(self.root, None)

    def get_tree(self, name, params=''):
        partitions = []
        self.collect_partitions(self.root, partitions)
        tree = {
            'partitions': partitions,
            'pts_idx': self.pts
        }
        return tree

    def collect_partitions(self, node, array):
        array.append({
            'id': node.id,
            'lvl': node.persistence,
            'span': [node.span[0], node.span[1]],
            'minmax_idx': [node.min_idx, node.max_idx],
            'merge': 'max' if node.is_max_merge else 'min',
            'parent': node.parent.id if node.parent is not None else None,
            'children': [child.id for child in node.children] if node.persistence > 0 else []
        })

        self.check_partition(node)

        if node.persistence > 0:
            if len(node.children) > 2:
                print('\t{} has {} children at level {}'.format(node.id, len(node.children), node.persistence))
            for child in node.children:
                self.collect_partitions(child, array)

    #
    # verify
    #

    def verify(self):
        if self.debug:
            self.statistics()
        return self

    def statistics(self):
        levels = defaultdict(list)
        self.stat(self.root, levels)
        n = 0
        b = 0
        for level in levels.keys():
            if level > 0:
                n += len(levels[level])
            else:
                b = len(levels[level])
        print('\tstatistics: {} levels {} base, {} new'.format(len(levels), b, n))
        # for level in sorted(levels.keys()):
        #     print("{:.2g} {}".format(level, len(levels[level])))

    def stat(self, node, levels):
        levels[node.persistence].append(node)
        if node.persistence > 0:
            for child in node.children:
                self.stat(child, levels)

