from slippi import Game
from slippi.event import Start
import sys
import os

from slippi.parse import parse
from slippi.event import ParseEvent

def main():
    winnersList = []
    winnersDict = {}
    numOfGamesDict = {}
    fileName = 'SmallReplays/'
    entries = getFileEntries(fileName)
    
    for entry in entries:
       
        if entry[-3:] == 'slp':
           
            g = Game(fileName + entry)
            frames = g.frames
            ports = frames[0].ports

            
            # XYPositionChange(g)
            # healthChanged(g)
            # printCharacters(ports)
            # landedAttacks(g)
            winners = getWinner(g)
            winnersDict = UpdateWinnersDictionary(winners, winnersList, winnersDict)
            # gameStockRecap(g)

            for port in ports:
                if port != None:
                    character = str(port.leader.post.character)
                    charExist = numOfGamesDict.get(character)
                    if charExist == None:
                        numOfGamesDict[character] = 1
                    else:
                        numOfGamesDict[character] += 1

    # printWinnersDict(winnersDict)
    character = 'InGameCharacter.SHEIK'
    # printNumOfGamesDict(numOfGamesDict)    
    charWins = winnersDict[character]
    charNumOfGames = numOfGamesDict[character]
    charWinPercentage = round((float(charWins / charNumOfGames) * 100), 2)

    print( character + "'s win percentage is: " + str(charWinPercentage) + "%")


def printWinnersDict(winnersDict):                 
    for character in winnersDict:
        print(str(character) + " has this " + str(winnersDict[character]) + " wins.")

def printNumOfGamesDict(numOfGamesDict):
    for character in numOfGamesDict:
        print(str(character) + " appear in " + str(numOfGamesDict[character]) + " games.")



    

def UpdateWinnersDictionary(winners, winnersList, winnersDictionary):
    for winner in winners:
        winnersList.append(winner)
        winnerForDict = winnersDictionary.get(winner)
        if winnerForDict == None:
            winnersDictionary[winner] = 1
        else:
            winnersDictionary[winner] += 1

    return winnersDictionary

    

    



def getWinner(g):
    """Return the winner of a match """
    
    lastFrame = g.frames[-1]

    ports = lastFrame.ports
    winners = []
    for port in ports:
        if port != None:
            player = port.leader.post

            if player.stocks != 0:
                # print("This character won " + str(player.character))
                name = str(player.character)
                winners.append(name)

        
    # print('------------------------\n')   
    return winners

def getFileEntries(fileName):
    files = os.listdir(fileName)
    entries = []
    for theFile in files:
        if theFile[-3:] == 'slp':
            entries.append(theFile)
   
    
    return entries

def gameStockRecap(g):
    for index in range(len(g.frames) - 1):
        lossStock(g.frames[index],g.frames[index + 1])

    for port in g.frames[-1].ports:

        if port != None and port.leader.post.stocks == 0:
            print("This character lost " + str(port.leader.post.character))
            print("They were killed by marth")
            deadCharacter = str(port.leader.post.character)
            isOver = EndGame(g.frames)
    print('------------------------\n')        


# def lastCharacterToAttack(g, currentFrameIndex, nextFrameIndex):
#     """ This will return the last character that attacked """
#     for port in g.frames[currentFrameIndex].ports:
        
#         pass

def EndGame(frames):
        """ Returns true if the game ends and says who killed who"""
        ports = frames[-1].ports
        for port in ports:
            if port != None and port.leader.post.stocks == 0:
                deadCharacter = str(port.leader.post.character)
                print("The move that killed " + deadCharacter + " was " + str(port.leader.post.last_attack_landed)) 
                return True
        return False

def landedAttacks(g):    

    frames = g.frames
    for portIndex in range(len(frames[0].ports)):
        if frames[0].ports[portIndex] != None:
            player = frames[0].ports[portIndex].leader.post
        
            printCharacterPort(player)
            for framesIndex in range(len(g.frames)-1):
                player = frames[framesIndex].ports[portIndex].leader.post
                playerNext = frames[framesIndex + 1].ports[portIndex].leader.post
                if player.last_attack_landed != None and player.last_attack_landed != playerNext.last_attack_landed:
                    print(player.last_attack_landed)
        
        


def printCharacterPort(playerOne):
    print("The character's name is " + str(playerOne.character))


def printCharacters(ports):
    print('----------------------------')
    for port in ports:
        if port != None:
            character = port.leader.post.character

            print("The characters are " + str(character))
    print('----------------------------\n')

def printGameStartAndEnd(g):
    s = g.start
    e = g.end
    print(s)
    print('\n\n')
    print(e)
    
    
def printMetadata(g):    
    print(g.metadata)

def healthChanged(g):
    frames = g.frames
    for index in range(len(g.frames)-15):
        StartDamage = frames[index].ports[0].leader.post.damage 
        EndDamage = frames[index + 1].ports[0].leader.post.damage 
        lossStock(frames[index],frames[index+1])
        if StartDamage != EndDamage:
            healthChange = EndDamage - StartDamage
            print("\nThe previous health was " + str(StartDamage))
            print("\nThe new health is " + str(EndDamage))
            print("\nThe change was by " + str(healthChange))

def lossStock(frame,nextFrame):
    
    for index in range(len(frame.ports)):
        if frame.ports[index] != None:
            character = str(frame.ports[index].leader.post.character)
       
            currentStockCount = frame.ports[index].leader.post.stocks
            nextStockCount = nextFrame.ports[index].leader.post.stocks
            if nextStockCount != currentStockCount:
                print("\nThis is for character " + character)
                print("\nThis player had " + str(currentStockCount))
                print("\nThey now have " + str(nextStockCount))

def XYPositionChange(g):

    for index in range(len(g.frames)-15):
        frames = g.frames
        startData = frames[index].ports[0].leader # see also: port.follower (ICs)
        endData = frames[index + 5].ports[0].leader

        xPosition = endData.post.position.x - startData.post.position.x
        yPosition = endData.post.position.y - startData.post.position.y

        if xPosition >= 5:
            print("\nThe x position changed by " + str(xPosition))
        
        if yPosition >= 20:
            print("\nThe y position changed by " + str(yPosition))

   

main()