"""
This is a temporary file for testing.
This directly passes the normalised tree and not the behaviour trees, unlike the setup in actual code.
"""

from classes.normalised_tree import NormalisedTree
from classes.generation import Generation
from utils.generateTree import generateInitialTrees

# parents = [-1, 0, 1, 1, 1, 1, 0, 6, 6, 6]
# labels = ["R", "A", "A", "B", "A", "B", "A", "A", "A", "B"]
# nt1 = NormalisedTree(parents, labels)
# parents = [-1, 0, 0]
# labels = ["A", "A", "B"]
# nt2 = NormalisedTree(parents, labels)

firstGeneration = generateInitialTrees(numTrees=5, depth2SizeLimit=4, depth3SizeLimit=5, SC=True)
for tree in firstGeneration:
    tree.displayTree()

generation = Generation(firstGeneration, DC=True, SC=True)
frequent_patterns = generation.getFrequentPatterns()

for pat in frequent_patterns:
    print(pat.getParentArray(), pat.getLabelArray(), sep="\n")
    print("-----")

generation = generation.getNextGeneration()
print("Now have new generation")

for tree in generation.getTopTrees(generation.pop):
    tree.displayTree()
