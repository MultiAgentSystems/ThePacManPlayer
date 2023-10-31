"""
Represents a normalised tree, which is represented using a parent array and a label array.
The labels for Selection and Condition nodes are the same as the name of the node.
The labels for Action/Condition nodes are the name of the node followed by the description of the action/condition.
The nodes are numbered in their preorder traversal order, from 0 to n-1.
"""


class NormalisedTree:
    def __init__(self, parents, labels) -> None:
        self.parents = parents.copy()
        self.labels = labels.copy()
        self.sz = len(parents)
        self.children = [[] for _ in range(self.sz)]
        for i in range(self.sz):
            if self.parents[i] != -1:
                self.children[self.parents[i]].append(i)

    def getParentArray(self):
        return self.parents

    def getLabelArray(self):
        return self.labels

    def getSize(self):
        return self.sz

    def getKthParent(self, node, k):
        for _ in range(k):
            node = self.parents[node]
        return node

    def getNextSibling(self, node):
        parent = self.parents[node]
        if parent == -1:
            return -1
        for i in range(len(self.children[parent])):
            if self.children[parent][i] == node:
                if i == len(self.children[parent]) - 1:
                    return -1
                else:
                    return self.children[parent][i + 1]

    def updateRMOs(self, rmos, up, label):
        # Takes the RMOs of a pattern, along with the number of
        # 'up' steps to take from the rightmost leaf to attach a new node 'label'
        # Returns the new RMOs
        new_rmos = []
        assert (rmos == sorted(rmos))
        check = None
        for x in rmos:
            if up == 0:
                if len(self.children[x]) == 0:
                    continue
                y = self.children[x][0]
            else:
                y = self.getKthParent(x, up - 1)
                assert y != -1
                if self.parents[y] == check:
                    # All RMOs that can be found in this sibling line have already been explored
                    continue
                y = self.getNextSibling(y)
                if y == -1:
                    continue
                check = self.parents[y]

            while y != -1:
                if self.labels[y] == label:
                    new_rmos.append(y)
                y = self.getNextSibling(y)

        assert (len(set(new_rmos)) == len(new_rmos))
        return new_rmos

    def expandPatterns(self, pat_rmos):
        # Takes pat_rmos = {NormalisedTree of the pattern: [indices of RMOs]}
        # Returns new expanded patterns with their RMOs in the same format
        possible_labels = list(set(self.getLabelArray()))
        expanded_pats = {}

        for pat, rmos in pat_rmos.items():
            curr_extender = pat.getSize() - 1
            for p in range(self.sz):
                for new_label in possible_labels:
                    new_rmos = self.updateRMOs(rmos, p, new_label)
                    if len(new_rmos) == 0:
                        continue

                    new_parents = pat.getParentArray().copy()
                    new_labels = pat.getLabelArray().copy()
                    new_parents.append(curr_extender)
                    new_labels.append(new_label)
                    new_pat = NormalisedTree(new_parents, new_labels)
                    assert (new_pat not in expanded_pats)
                    expanded_pats[new_pat] = new_rmos

                curr_extender = pat.getKthParent(curr_extender, 1)
                if curr_extender == -1:
                    break

        return expanded_pats

    def getTerminals(self):
        is_leaf = [True] * len(self.parents)
        for parent in self.parents[1:]:
            is_leaf[parent] = False
        terminals = []
        for i in range(len(is_leaf)):
            if is_leaf[i]:
                terminals.append(i)
        return terminals

    def countTerminals(self):
        return len(self.getTerminals())

    def invalidTerminalsExist(self):
        terminals = self.getTerminals()
        for terminal in terminals:
            if self.labels[terminal] in ["SelectorNode", "SequenceNode"]:
                return True
        return False

    def getNormalisedTree(self):
        return self

    def __hash__(self):
        return hash((tuple(self.parents), tuple(self.labels)))

    def __eq__(self, other):
        return (self.parents, self.labels) == (other.parents, other.labels)
