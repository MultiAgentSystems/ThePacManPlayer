from pythonPacMan.runGame import runGame

def fitness(tree) -> float:
    gameScore = runGame(numRuns=3, BT=tree)
    treeSize = len(tree.getExecutionOrder())
    parsimonyCoefficient = 7

    treeScore = gameScore - parsimonyCoefficient * treeSize
        
    print(treeScore)
    return treeScore
