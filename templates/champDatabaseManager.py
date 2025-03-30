import sqlite3

import championSkinDataReader


def connect():
    connection=sqlite3.connect(r"resource\leagueChampSkins.sqlite3")
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM skins"
        cursor.execute(query)
    except sqlite3.OperationalError:
        createTables(connection)
    return connection

def reset(connection):
    cursor = connection.cursor()
    query = "DROP TABLE skins"
    cursor.execute(query)
    connection.commit()
    connection.close()

def createTables(connection):
    cursor = connection.cursor()
    query = "CREATE TABLE IF NOT EXISTS skins (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, skin_name VARCHAR(255) NOT NULL UNIQUE, champion_name VARCHAR(255) NOT NULL);"
    cursor.execute(query)

# uses method from championSkinDataReader to fill data up in sqlite3
def populateData(connection):
    arraySkinChamp=championSkinDataReader.getSkinInfos()
    cursor = connection.cursor()
    for skin in arraySkinChamp:
        try:
            query = "INSERT INTO skins (skin_name,champion_name) VALUES(\""+skin[0]+"\",\""+skin[1]+"\");"
            cursor.execute(query)
        except:
            continue
    connection.commit()
    
#returns original champion name. If it doesn't exist in the database, then update the database and rerun it.
def getChampion(connection,skinName):
    cursor = connection.cursor()
    query = "SELECT champion_name FROM skins WHERE champion_name = \""+skinName+"\";"
    cursor.execute(query)
    
    isChampion = cursor.fetchone()
    if isChampion:
        return skinName
    
    query = "SELECT champion_name FROM skins WHERE skin_name = \""+skinName+"\";"
    cursor.execute(query)
    
    isSkin = cursor.fetchone()
    if isSkin:
        return isSkin[0]
    cursor.close()
    populateData(connection)
    return getChampion(connection,skinName)


    
# connection = connect()

# print(getChampion(connection,"God-King Garen"))
