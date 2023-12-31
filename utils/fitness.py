from pythonPacMan.runGame import runGame

def fitness(tree) -> float:
    gameScore = runGame(numRuns=5, BT=tree)
    treeSize = len(tree.getExecutionOrder(update = True))
    parsimonyCoefficient = 0.7

    treeScore = gameScore - parsimonyCoefficient * treeSize
        
    # print(treeScore)
    return treeScore
