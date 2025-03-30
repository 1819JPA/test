from bs4 import BeautifulSoup
import requests

# returns a list of tuple (skin_name,champion_name)
def getSkinInfos():
    try:
        arraySkinChamp=[]
        link='https://leagueoflegends.fandom.com/wiki/List_of_champion_skins_(League_of_Legends)'
        source = requests.get(link,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}).text
        soup = BeautifulSoup(source,"html.parser")
        allSkinInfos = soup.find_all("td",{"class": "skin-icon"})
        for skin in allSkinInfos:
            arraySkinChamp.append((skin.getText(),skin.get("data-champion")))
        return arraySkinChamp
    except:
         print("Error in getting skins information")
         return []

#getSkinInfos()