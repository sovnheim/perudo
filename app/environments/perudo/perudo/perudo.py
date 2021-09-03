import numpy as np 
import itertools

# utils
def rollDice(dType=6):
    return np.random.randint(1, dType+1)

def choose(options):
    return options[np.random.randint(0, len(options))]

class GameParameters():
    "Class GameParameters contain parameters for game initialization"
    def __init__(self):
        self.diceType = 6
        self.diceCount = 5
        self.players = ["alice", "bob", "cecile"]
        pass

class Player():
    def __init__(self, params: GameParameters):
        self.params = params
        self.diceRolls = []
        self.remainingDice = params.diceCount

    def setDiceRolls(self):
        self.diceRolls = [rollDice(self.params.diceType) for i in range(0, self.remainingDice)]
    
    def removeDice(self):
        self.remainingDice -= 1
        

class Perudo():
    def __init__(self, params: GameParameters):
        self.players = {player: Player(params) for player in params.players}
        self.params = params

        self.bids = []
        self.turns = 0

    def getTotalDiceCount(self):
        "returns count of dice in self.playerDice"
        return sum([self.players[player].remainingDice for player in self.players])

    def getLegalBids(self):
        "return list of legal bids based on current GameState"
        if len(self.bids) < 1: 
            lastBid = (1,1)
        else:
            lastBid = self.bids[-1]

        legalDiceCountOptions = [diceCount for diceCount in range(lastBid[0], self.getTotalDiceCount()+1)]
        legalDiceSideOptions = [diceSide for diceSide in range(lastBid[1], self.params.diceType +1)]

        return list(
            itertools.chain(
                *[[(diceCount, diceSide) 
                for diceCount in legalDiceCountOptions 
                if (diceCount, diceSide) not in self.bids] 
                for diceSide in legalDiceSideOptions]))

    def getGameRunningStatus(self): # to be removed
        "return True if game has players that can make a move"
        if self.getTotalDiceCount() > 1: return True
        else: return False
    
    def hasAWinner(self):
        activePlayers = 0
        for player in self.players:
            if self.players[player].remainingDice > 0: activePlayers +=1
        if activePlayers <= 1:
            return True
        else: 
            return False
    
    def getWinner(self):
        if self.hasAWinner():
            print(" | | | {} wins the game".format(list(self.players.keys())[0]))
            return list(self.players.keys())[0]

    def callBullshit(self, statement, caller):
        "Evaluates statement and removes dice accordingly"
        allDice = list(itertools.chain(*[self.players[player].diceRolls for player in self.players]))
        players = [player for player in perudo.players]
        if len([diceSide for diceSide in allDice if diceSide == statement[1]]) < statement[0]:
            liar = players[players.index(caller)-1]
        else:
            liar = caller

        if perudo.players[liar].remainingDice > 1: 
            print(" | | {} loses a dice".format(liar))
            perudo.players[liar].removeDice()
        else:
            print(" | | {} exits the game".format(liar)) 
            perudo.players.pop(liar)

    def setPlayersDiceRolls(self):
        "Handles dice rolls for players"
        for player in self.players:
            self.players[player].setDiceRolls()
            print(player, self.players[player].diceRolls)

    def runGameRound(self):
        "loops through a single round of the game, from dice roll to losing a die"

        self.setPlayersDiceRolls()
        roundIsRunning = True
        caller = ""

        while roundIsRunning is True and self.hasAWinner() is False:
            for player in [player for player in self.players if self.players[player].remainingDice >= 1]:
                legalMoves = []
                if len(self.getLegalBids()) >= 1: legalMoves.append("bid")
                if len(self.bids) > 1: 
                    legalMoves.append('bullshit')

                playerMove = choose(legalMoves)

                if playerMove == "bid":
                    bid = choose(self.getLegalBids())
                    self.bids.append(bid)
                    print(" | {} bids {}".format(player, bid))
                if playerMove == "bullshit":
                    caller = player
                    roundIsRunning = False
                    print(" | {} calls BS".format(player))
                    break
        
        self.callBullshit(self.bids[-1], caller)

    def startGame(self):
        "Game main loop which executes rounds until there is a winner"
        while self.hasAWinner() == False:
            self.runGameRound()
        
        self.getWinner()


#let's go
params = GameParameters()
perudo = Perudo(params)

perudo.startGame()
