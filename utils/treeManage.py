
import pickle
import time

SESSION_ID = str(time.time()).split(".")[0]

def saveTree( behaviourTree, filename, directory ):
    #Use pickle to save the tree.
    filename = "./agentEvolution/" + directory + "/" + filename
    filename += "_" + str( SESSION_ID )
    filename += ".pickle"

    with open( filename, 'wb' ) as f:
        pickle.dump( behaviourTree, f , pickle.HIGHEST_PROTOCOL )

def loadTree( filename, directory ):
    filename = "./agentEvolution/" + directory + "/" + filename
    filename += "_" + str( SESSION_ID )
    filename += ".pickle"

    with open( filename, 'rb' ) as f:
        return pickle.load( f )

