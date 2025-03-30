# gets player info and string from image by calling methods from imageToString.py
# goes through the list of champions and skins then returns player info and champion name
# if the skin name does not exist in the database, rerun connection in champDatabaseManager to 

import champDatabaseManager
import imageToString

def convertToChampionName(names):
    champion_names=[]
    connection = champDatabaseManager.connect()
    for name in names:
        champion_names.append(champDatabaseManager.getChampion(connection,name))
    return champion_names

def getChampionNames():
    names=imageToString.convertImagetoString()
    return convertToChampionName(names)

# print(getChampionNames())