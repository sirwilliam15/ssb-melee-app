from slippi import Game
from slippi.event import Start
import sys

from slippi.parse import parse
from slippi.event import ParseEvent

def main():
    g = Game('MarthPikachu20191030.slp')
    frames = g.frames
    ports = frames[0].ports
    
    # XYPositionChange(g)
    # healthChanged(g)
    printCharacters(ports)
    # landedAttacks(g)

    # gameStockRecap(g)

def gameStockRecap(g):
    for index in range(len(g.frames) - 10):
        lossStock(g.frames[index],g.frames[index + 1])

    for port in g.frames[-1].ports:

        if port != None and port.leader.post.stocks == 0:
            print("This character lost " + str(port.leader.post.character))
            print("They were killed by marth")
            deadCharacter = str(port.leader.post.character)
            EndGame(deadCharacter,g.frames[-1].ports)
        



def EndGame(deadCharacter,ports):

        for port in ports:
            if port != None and port.leader.post.stocks != 0:
                print("The move that killed " + deadCharacter + " was " + str(port.leader.post.last_attack_landed)) 







def landedAttacks(g):    

    frames = g.frames
    playerOne = frames[0].ports[0].leader.post
    printCharacterPort(playerOne)
    for index in range(len(g.frames)-15):
        playerOne = frames[index].ports[0].leader.post
        playerOneNext = frames[index + 1].ports[0].leader.post
        if playerOne.last_attack_landed != None and playerOne.last_attack_landed != playerOneNext.last_attack_landed:
            print(playerOne.last_attack_landed)
        
        


def printCharacterPort(playerOne):
    print("The character's name is " + str(playerOne.character))


def printCharacters(ports):
    for port in ports:
        if port != None:
            character = port.leader.post.character

            print("The characters are " + str(character))

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