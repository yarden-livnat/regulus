from collections import defaultdict


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

    def __init__(self, persistence, base_pts=None, min_idx=None, max_idx=None, from_partition=None, is_max=None):
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

        if from_partition is not None:
            self.min_idx = from_partition.min_idx
            self.max_idx = from_partition.max_idx
            self.children.append(from_partition)
            from_partition.parent = self

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        # if child.min_idx != self.min_idx and child.max_idx != self.max_idx:
        #     print("ERROR: child {} [{} {}] merged into parent {} [{} {}] without a matching extrema".format(child.id,
        #                                             child.min_idx, child.max_idx, self.id, self.min_idx, self.max_idx))


class Builder(object):
    def __init__(self, debug=False):
        self.base = None
        self.merges = []
        self.maxima = set()
        self.min_map = defaultdict(set)
        self.max_map = defaultdict(set)
        self.active = set()
        self.root = None
        self.pts = []
        self.original_pts = set()
        self.debug = debug
        self.mapping = dict()
        self.unique = set()
        self.hierarchy = None

        self.all = dict()
        self.data_pts = []
        self.single = 0

    def data(self, pts):
        self.data_pts = pts
        return self

    def msc(self, base, hierarchy):
        self.base = base
        self.hierarchy = hierarchy
        return self

    def build(self):
        self.prepare()
        self.merge()

        # get root
        if len(self.active) != 1:
            print(len(self.active), 'active')
            for p in self.active:
                print(f'{p.id}: {p.min_idx} {p.max_idx}  pts={p.base_pts}')
                if len(p.children) > 0:
                    print('\t', [c.id for c in p.children])
            raise RuntimeError('Error: found {} roots'.format(len(self.active)))
        self.root = self.active.pop()

        self.single = 0
        idx = self.build_idx(self.root, 0)
        print('found {} singles'.format(self.single))
        print('len(idx)=', idx)

        self.test_uniques()

        self.pts.extend([self.root.min_idx, self.root.max_idx])
        self.rename(self.root, 0)
        return self

    # internal

    def merge(self):
        for record in self.merges:
            # print(record.level, record.is_max, record.src, record.dest)
            if record.src == record.dest:
                continue

            # degenerate case: merge.dest may have been merged already (same persistence level)
            dest = self.current(record.dest)
            src = self.current(record.src)
            if src == dest:
                print("\t degenerated case:", src, dest)
                continue

            record.dest = dest
            record.src = src
            self.mapping[record.src] = record.dest

            if record.is_max:
                self.collapse(record, self.max_map, lambda item: item.min_idx)
            else:
                self.collapse(record, self.min_map, lambda item: item.max_idx)

    def prepare(self):
        PartitionNode.reset()
        for key, pts in self.base.items():
            p = PartitionNode(0, pts.tolist(), key[0], key[1])
            self.maxima.add(key[1])
            self.add(p)
        print('starting with ', len(self.active), 'partitions')

        for key, record in self.hierarchy.items():
            is_max = key in self.maxima
            self.merges.append(Merge(record[0], is_max, key, record[1]))

        # self.find_unique()
        # self.remove_non_unique()

        self.merges.sort(key=lambda m: (m.level, m.src))
        high = self.merges[-1].level
        for merge in self.merges:
            merge.level /= high

        if self.debug:
            for partition in self.active:
                self.check_partition(partition)

    def collapse(self, merge, idx_map, idx):
        add_partitions = []
        remove_partitions = set()

        for d in idx_map[merge.dest]:
            new_partition = None
            remove_src = set()
            for s in idx_map[merge.src]:
                if idx(s) == idx(d):
                    if s.persistence != merge.level:
                        if new_partition is None:
                            new_partition = PartitionNode(merge.level, from_partition=d, is_max=merge.is_max)
                            remove_partitions.add(d)  # can't be removed during the iterations
                            add_partitions.append(new_partition)
                        new_partition.add_child(s)
                    else:
                        # s is an intermediate and should be absorbed
                        if len(s.children) == 0:
                            # s is a base partition
                            d.base_pts.extend(s.base_pts)
                        else:
                            for child in s.children:
                                d.add_child(child)
                        if len(s.extrema) > 0:
                            d.extrema.extend(s.extrema)
                    remove_src.add(s)  # can't be removed during the iterations
            for s in remove_src:
                self.remove(s)

        for s in idx_map[merge.src]:
            # create a new partition with a single child because the max value has changed
            new_partition = PartitionNode(merge.level, from_partition=s)
            if merge.is_max:
                new_partition.max_idx = merge.dest
            else:
                new_partition.min_idx = merge.dest
            add_partitions.append(new_partition)

        for r in remove_partitions | idx_map[merge.src]:
            self.remove(r)

        # removed for topopy ver 1.0 because it assign each extrema to one base partition
        # assign the eliminated extrema as an extra internal point to the first new partition
        # if merge.src not in self.unique:
        #     if len(add_partitions) > 0:
        #         target = add_partitions[0]
        #     else:
        #         target = next(iter(idx_map[merge.dest]))
        #     target.extrema.append(merge.src)

        for new_partition in add_partitions:
            self.add(new_partition)

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
                    if idx in p.base_pts:
                        p.base_pts.remove(idx)
                        print(f'{p.id}: removed non unique')
                    else:
                        print(f'{p.id}: min/max not found')
                else:
                    print(idx, 'not removed because it is unique')

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
            # if partition.min_idx in partition.base_pts and partition.min_idx not in self.unique:
            #     print('*** WARNING: min_idx {} in partition {}'.format(partition.min_idx, partition.id))
            # if partition.max_idx in partition.base_pts and partition.max_idx not in self.unique:
            #     print('*** WARNING: max_idx {} in partition {}'.format(partition.max_idx, partition.id))

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

    def test_uniques(self):
        for u in self.unique:
            self.test_unique(u, self.root, 0)

    def test_unique(self, u, node, lvl):
        if u == node.min_idx:
            print('unique {} is min_idx for node {} lvl {}'.format(u, node.id, lvl))
        if u == node.max_idx:
            print('unique {} is max_idx for node {} lvl {}'.format(u, node.id, lvl))
        if u in node.extrema:
            print('unique {} in extrema for node {} lvl {}'.format(u, node.id, lvl))
        if node.span[0] <= u < node.span[1]:
            print('unique {} in span for node {} lvl {}'.format(u, node.id, lvl))
        for child in node.children:
            self.test_unique(u, child, lvl+1)

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
