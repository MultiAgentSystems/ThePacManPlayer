def DecisionSimulator( behaviourTree, player) -> str:
    '''
        Should return one of the four predefined actions : 'L', 'R', 'U', 'D', 'E'.
    '''
    try : 
        if behaviourTree is None:
            return 'E'
        
        treeRoot = behaviourTree.getRoot()

        response = treeRoot.makeDescision(player)

        # print(f" ActionToPerform : {response['action']}")
        return response['action']
    except Exception:
        return 'E'
