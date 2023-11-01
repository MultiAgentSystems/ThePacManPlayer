"""
This is a temporary file for testing.
This directly passes the normalised tree and not the behaviour trees, unlike the setup in actual code.
"""

from classes.normalised_tree import NormalisedTree
from classes.generation import Generation

parents = [-1, 0, 1, 1, 1, 1, 0, 6, 6, 6]
labels = ["R", "A", "A", "B", "A", "B", "A", "A", "A", "B"]
nt1 = NormalisedTree(parents, labels)
parents = [-1, 0, 0]
labels = ["A", "A", "B"]
nt2 = NormalisedTree(parents, labels)
generation = Generation([nt1, nt2])
frequent_patterns = generation.getFrequentPatterns()

for pat in frequent_patterns:
    print(pat.getParentArray(), pat.getLabelArray(), sep="\n")
    print("-----")
