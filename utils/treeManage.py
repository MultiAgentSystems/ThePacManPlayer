
import pickle
import time
SESSION_ID = "1699119758"

def saveTree( behaviourTree, filename, directory ):
    #Use pickle to save the tree.
    filename = "./agentEvolution/" + directory + "/" + filename
    filename += "_" + str( SESSION_ID )
    filename += ".pickle"

    with open( filename, 'wb' ) as f:
        pickle.dump( behaviourTree, f , pickle.HIGHEST_PROTOCOL )

def loadTree( filename, directory ):
    name = "Gen11_2266_1699114825"
    filename = "./agentEvolution/" + directory + "/" + filename
    filename += "_" + str( SESSION_ID )
    filename += ".pickle"

    with open( filename, 'rb' ) as f:
        return pickle.load( f )

