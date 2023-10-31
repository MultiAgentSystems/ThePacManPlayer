from logs.logger import Logger
from .normalised_tree import NormalisedTree
from math import ceil


def score(tree) -> float:
    return 1.0 if tree is not None else 0.0


class Generation:
    def __init__(self, trees=None, logger=None) -> None:
        self.trees = trees if trees is not None else [];
        self.treeScores = {}
        self.logger = logger if logger is not None else Logger()
        self.topCount = 10

        # FREQT constants, apart from topCount
        self.minSup = int(ceil(0.3 * self.topCount))
        self.minTerminals, self.maxTerminals = 2, 15
        self.minNodes = 3

    def scoreGeneration(self) -> dict:
        for tree in self.trees:
            self.treeScores[tree] = 0

        self.treeScores = dict(sorted(self.treeScores.items(), key=lambda item: item[1], reverse=True))
        return self.treeScores

    def getTopK(self, k) -> list:
        if (self.treeScores is None):
            self.scoreGeneration()
        return list(self.treeScores.keys())[:k]

    def isValidPattern(self, pat):
        nodes, terminals = len(pat.getParentArray()), pat.countTerminals()
        return nodes >= self.minNodes and terminals >= self.minTerminals and terminals <= self.maxTerminals

    def getFrequentPatterns(self):
        bts = [tree.getNormalisedTree() for tree in self.getTopK(self.topCount)]
        bt_parents = [bt.getParentArray() for bt in bts]
        bt_labels = [bt.getLabelArray() for bt in bts]

        k_pats = {}
        final_pats = []

        for bt_idx in range(self.topCount):
            pars, labels = bt_parents[bt_idx], bt_labels[bt_idx]
            n = len(pars)
            for i in range(n):
                pat = NormalisedTree([-1], labels[i])
                k_pats[pat][bt_idx] = [i]
                if self.isValidPattern(pat):
                    final_pats.append(pat)

        max_bt_size = max([len(pars) for pars in bt_parents])
        for k in range(2, max_bt_size + 1):
            new_k_pats = {}
            old_pats_per_bt = [{} for _ in range(self.topCount)]

            for pat, rmos in k_pats.items():
                for bt_idx, rmo in rmos.items():
                    old_pats_per_bt[bt_idx][pat] = rmo

            for bt_idx in range(self.topCount):
                expanded_pats = bts[bt_idx].expandPatterns(old_pats_per_bt[bt_idx])
                for pat, rmos in expanded_pats.items():
                    if pat not in new_k_pats:
                        new_k_pats[pat] = {}
                    new_k_pats[pat][bt_idx] = rmos

            k_pats = {}
            for pats, rmos in new_k_pats.items():
                # len(rmos) will give the number of BTs in which the pattern occurs
                # We discard this pattern completely if it:
                # - doesn't have enough support: support will never increase on expanding
                # - has too many terminals: terminals will never decrease on expanding
                if len(rmos) < self.minSup or pats.countTerminals() > self.maxTerminals:
                    continue

                k_pats[pats] = rmos
                if self.isValidPattern(pats):
                    final_pats.append(pats)

        return final_pats

    def performCrossOver(self):
        pass

    def performMutation(self):
        pass
