

def DecisionSimulator( behaviourTree, player) -> dict:
    '''
        Should return one of the four predefined actions : 'L', 'R', 'U', 'D', 'E'.
    '''
    try : 
        if behaviourTree is None:
            return { 'Status' : 'Error', 'Result' : 'E' }
        
        treeRoot = behaviourTree.getRoot()

        state, decision = treeRoot.makeDescision(player)

        return { 'Status' : state, 'Result' : decision }
    except Exception:
        return { 'Status' : 'Error', 'Result' : 'E' }
