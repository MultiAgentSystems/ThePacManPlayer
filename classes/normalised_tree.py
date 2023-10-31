"""
Represents a normalised tree, which is represented using a parent array and a label array.
The labels for Selection and Condition nodes are the same as the name of the node.
The labels for Action/Condition nodes are the name of the node followed by the description of the action/condition.
The nodes are numbered in their preorder traversal order, from 0 to n-1.
"""


class NormalisedTree:
    def __init__(self, parents, labels) -> None:
        self.parents = parents
        self.labels = labels

    def getParentArray(self):
        return self.parents

    def getLabelArray(self):
        return self.labels

    def expandPatterns(self, pat_rmos):
        # Takes pat_rmos = {NormalisedTree of the pattern: [indices of RMOs]}
        # Returns new expanded patterns with their RMOs in the same format
        return {}

    def countTerminals(self):
        is_leaf = [True] * len(self.parents)
        for parent in self.parents:
            is_leaf[parent] = False
        return sum(is_leaf)

    def __hash__(self):
        return hash((self.parents, self.labels))

    def __eq__(self, other):
        return (self.parents, self.labels) == (other.parents, other.labels)
