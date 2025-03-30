import findChampion
import opggReader
import imageCapture
import time
def main():
    names = findChampion.getChampionNames()
    switchOrderIfTopIsNotMyTeam(names)
    winrates = opggReader.getTeamWinrate(names)
    print(winrates[5])

def switchOrderIfTopIsNotMyTeam(names):
    if not imageCapture.isTopMyTeam:
        for i in range(5):
            temp=names[i]
            names[i]=names[i+5]
            names[i+5]=temp

main()