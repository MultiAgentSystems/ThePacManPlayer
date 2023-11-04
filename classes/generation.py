from .normalised_tree import NormalisedTree
from .nodes import ActionNode, ConditionNode, SelectorNode, SequenceNode
from math import ceil
from utils.fitness import fitness
import random
from concurrent.futures import ProcessPoolExecutor, as_completed

from utils.generateTree import generateNodes
from utils.conditions import ConditionFunctions
from utils.actions import ActionFunctions


class Generation:
    def __init__(self, trees=None, DC=True, SC=True) -> None:
        self.trees = trees if trees is not None else [];
        # self.tree_scores = [fitness(tree) for tree in self.trees]
        
        results = [0] * len(self.trees)
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(fitness, tree): tree for tree in self.trees}

            for future in as_completed(futures):
                tree = futures[future]
                index = self.trees.index(tree)
                results[index] = future.result()

        self.tree_scores = results
        
        self.averageTreeScore = sum(self.tree_scores) / len(self.tree_scores)

        # GP constants
        self.mutation_prob = 0.1
        self.cross_prob = 0.8
        self.pop = min(100, len(trees))
        self.tourn_size = 5
        self.gamma = 0.9

        # Constraints
        self.DC = DC
        self.SC = SC

        # FREQT constants, apart from topCount
        self.freqt_top_tree_ct = ceil(0.5 * len(self.trees))
        self.freqt_min_sup = ceil(0.6 * self.freqt_top_tree_ct)
        # TODO: Check their Ntptmin vs Ntpmin - do they limit the number of terminals or the number of nodes?
        # Right now, we're limiting the number of nodes.
        self.freqt_min_terminals, self.freqt_max_terminals = 2, 15
        self.freqt_min_nodes, self.freqt_max_nodes = 3, 15

        self.freq_patterns = self.getFrequentPatterns()
        # sort freq_patterns by size
        self.freq_patterns.sort(key=lambda x: x.getSize(), reverse=True)

    def getTopTrees(self, k) -> list:
        # Get the top k trees
        tree_idxes = list(range(len(self.trees)))
        tree_idxes.sort(key=lambda x: self.tree_scores[x], reverse=True)
        selected_trees = [self.trees[x] for x in tree_idxes[:k]]
        return selected_trees

    def tournamentSelect(self) -> list:
        # pick k random trees, and return the best one
        pool = random.sample(range(len(self.trees)), self.tourn_size)
        return self.trees[max(pool, key=lambda x: self.tree_scores[x])]

    def getNodePartition(self, tree):
        # Returns partition (protected_nodes, unprotected_nodes) from the tree
        protected_nodes = set()
        for pat in self.freq_patterns:
            pat_exec_order_labels = pat.getExecutionOrderLabels()
            for node in tree.getExecutionOrder()[1:]:
                if node in protected_nodes:
                    # Its entire subtree would be protected already (I think :P)
                    continue
                subtree_exec_order_labels = [i.getLabel() for i in node.getExecutionOrder(backtrack=True)]
                if subtree_exec_order_labels != pat_exec_order_labels:
                    continue
                # We have a match! Protect this subtree, except root
                subtree_exec_order = node.getExecutionOrder()
                for node in subtree_exec_order[1:]:
                    protected_nodes.add(node)

        unprotected_nodes = []
        for node in tree.getExecutionOrder()[1:]:
            if node not in protected_nodes:
                unprotected_nodes.append(node)

        return list(protected_nodes), unprotected_nodes

    def getNodeForCrossover(self, tree):
        if self.DC:
            protected, unprotected = self.getNodePartition(tree)
            protected_pick_prob = (self.gamma * len(protected)) / (len(protected) + len(unprotected))
            if random.random() < protected_pick_prob:
                return random.choice(protected)
            else:
                return random.choice(unprotected)
        else:
            return random.choice(tree.getExecutionOrder()[1:])

    def performCrossOver(self, tree1, tree2):
        # Pick a random node from tree1, and swap it with a random subtree from tree2
        # Returns the two new trees

        tree1_node, tree2_node = None, None
        for tries in range(100):
            node1, node2 = self.getNodeForCrossover(tree1), self.getNodeForCrossover(tree2)
            if (self.SC and node1._name == node2._name) or (not self.SC):
                tree1_node, tree2_node = node1, node2
                break

        if tree1_node is None or tree2_node is None:
            return tree1, tree2

        return (tree1.getCopyAfterReplacing(tree1_node, tree2_node),
                tree2.getCopyAfterReplacing(tree2_node, tree1_node))

    def performMutation(self, tree):
        # After getting the root, we need to recursively iterate 
        # through the tree and select a particular node for mutation.

        # Three kinds of mutation.

        threeWayToss = random.randint(0,2)
        
        allTheNodes = tree.getExecutionOrder(update = True)
        targetNode = None
        if ( len(allTheNodes) == 2 ):
            targetNode = allTheNodes[1]
        else :
            targetNode = allTheNodes[random.randint(1, len(allTheNodes) - 1)]    
        # Root node is not mutated.
        
        newNode = None
        if self.SC:
            if targetNode._name == "SelectorNode":
                newNode = generateNodes(unwanted=[3])[0]
            if targetNode._name == "SequenceNode":
                newNode = generateNodes(unwanted=[2])[0]
            if targetNode._name == "ConditionNode":
                newNode = generateNodes(specific=1)[0]
            if targetNode._name == "ActionNode":
                newNode = generateNodes(specific=0)[0]
        else:
            newNode = generateNodes()[0]
            
        if threeWayToss == 0:
            return tree.performChangeMutation(targetNode, newNode)
        elif threeWayToss == 1:
            return tree.performDeleteMutation(targetNode)
        else:
            # If the new generated node is selector or sequence, 
            # then we add two random children to it, a conidition
            # node and an action node.
            if ( isinstance(newNode, SelectorNode) or isinstance(newNode, SequenceNode) ):
                children = generateNodes(specific=1) + generateNodes(specific=0)
                newNode.addChild(children[0])
            return tree.performAdditionMutation(targetNode, newNode)

    def getNextGeneration(self):
        cross_ct = int(self.cross_prob * self.pop)
        copy_ct = self.pop - cross_ct
        next_gen = self.getTopTrees(copy_ct)
        assert cross_ct + copy_ct == self.pop
        for i in range(0, cross_ct, 2):
            par1, par2 = self.tournamentSelect(), self.tournamentSelect()
            child1, child2 = self.performCrossOver(par1, par2)
            next_gen.append(child1)
            if i + 1 < cross_ct:
                next_gen.append(child2)

        for i in range(self.pop):
            if random.random() < self.mutation_prob:
                next_gen[i] = self.performMutation(next_gen[i])

        return Generation(next_gen, DC=self.DC)

    def isValidPattern(self, pat):
        nodes, terminals = len(pat.getParentArray()), pat.countTerminals()
        return nodes >= self.freqt_min_nodes and terminals >= self.freqt_min_terminals and nodes <= self.freqt_max_nodes and not pat.invalidTerminalsExist()

    def getFrequentPatterns(self):
        bts = [tree.getNormalisedTree() for tree in self.getTopTrees(self.freqt_top_tree_ct)]
        bt_parents = [bt.getParentArray() for bt in bts]
        bt_labels = [bt.getLabelArray() for bt in bts]

        k_pats = {}
        final_pats = []

        for bt_idx in range(self.freqt_top_tree_ct):
            pars, labels = bt_parents[bt_idx], bt_labels[bt_idx]
            n = len(pars)
            for i in range(n):
                pat = NormalisedTree([-1], [labels[i]])

                if pat not in k_pats:
                    k_pats[pat] = {}
                    if self.isValidPattern(pat):
                        final_pats.append(pat)

                if bt_idx not in k_pats[pat]:
                    k_pats[pat][bt_idx] = []
                k_pats[pat][bt_idx].append(i)

        max_bt_size = max([bt.getSize() for bt in bts])
        for k in range(2, max_bt_size + 1):
            new_k_pats = {}
            old_pats_per_bt = [{} for _ in range(self.freqt_top_tree_ct)]

            for pat, bt_rmos in k_pats.items():
                for bt_idx, rmos in bt_rmos.items():
                    old_pats_per_bt[bt_idx][pat] = rmos

            for bt_idx in range(self.freqt_top_tree_ct):
                expanded_pats = bts[bt_idx].expandPatterns(old_pats_per_bt[bt_idx])
                for pat, bt_rmos in expanded_pats.items():
                    if pat not in new_k_pats:
                        new_k_pats[pat] = {}
                    new_k_pats[pat][bt_idx] = bt_rmos

            k_pats = {}
            for pats, bt_rmos in new_k_pats.items():
                # len(rmos) will give the number of BTs in which the pattern occurs
                # We discard this pattern completely if it:
                # - doesn't have enough support: support will never increase on expanding
                # - has too many terminals: terminals will never decrease on expanding
                if len(bt_rmos) < self.freqt_min_sup or pats.countTerminals() > self.freqt_max_terminals:
                    continue

                if pats not in k_pats and self.isValidPattern(pats):
                    final_pats.append(pats)
                k_pats[pats] = bt_rmos

        return final_pats
