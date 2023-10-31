from logs.logger import Logger


def score( tree ) -> float :
    return 1.0 if tree is not None else 0.0

class Generation : 
    def __init__(self, trees = None, logger = None) -> None:
        self.trees = trees if trees is not None else [];
        self.treeScores = {}
        self.logger = logger if logger is not None else Logger()

    def scoreGeneration(self) -> dict:
        for tree in self.trees:
            self.treeScores[tree] = 0

        self.treeScores = dict(sorted(self.treeScores.items(), key=lambda item: item[1], reverse=True))
        return self.treeScores

    def getTopK(self, k) -> list:
        if ( self.treeScores is None ):
            self.scoreGeneration()
        return list(self.treeScores.keys())[:k]

    def performCrossOver(self):
        pass

    def performMutation(self):
        pass
