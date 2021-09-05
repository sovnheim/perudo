import numpy as np
import gym
import itertools


def rollDice(dType=6):
    return np.random.randint(1, dType+1)


def choose(options):
    return options[np.random.randint(0, len(options))]


class GameParameters():
    "Class GameParameters contain parameters for game initialization"

    def __init__(self):
        self.diceType = 6
        self.diceCount = 3
        self.players = ["alice", "bob", "cecile"]
        self.gameLog = False
        self.debugLog = True


class Player():
    "Class Player container for player specific methods"

    def __init__(self, params: GameParameters):
        self.params = params
        self.diceRolls = []
        self.remainingDice = params.diceCount

    def setDiceRolls(self):
        self.diceRolls = [rollDice(self.params.diceType)
                          for i in range(0, self.remainingDice)]

    def removeDice(self):
        self.remainingDice -= 1


class PerudoEnv(gym.Env):
    def __init__(self, params: GameParameters):
        super(PerudoEnv, self).__init__()  # not sure what this does

        # game specific init
        self.name = 'perudo'
        self.players = {player: Player(params) for player in params.players}
        self.params = params
        self.rounds = 0

        # Env parameters for the selfplay wrapper
        self.n_players = len(params.players)
        # self.action_space = gym.spaces.Discrete(self.num_squares)
        self.observation_space = gym.spaces.Discrete(
            -1, 1, self.grid_shape+(2,))

    def getTotalDiceCount(self):
        "returns count of dice in self.playerDice"

        return sum([self.players[player].remainingDice for player in self.players])

    def getLegalBids(self, bids):
        "return list of legal bids based on current GameState"

        if len(bids) < 1:
            lastBid = (1, 1)
        else:
            lastBid = bids[-1]

        legalDiceCountOptions = [diceCount for diceCount in range(
            lastBid[0], self.getTotalDiceCount()+1)]
        legalDiceSideOptions = [diceSide for diceSide in range(
            lastBid[1], self.params.diceType + 1)]

        legalBids = list(
            itertools.chain(
                *[[(diceCount, diceSide)
                   for diceCount in legalDiceCountOptions
                   if (diceCount, diceSide) not in bids]
                  for diceSide in legalDiceSideOptions]))

        return legalBids

    def getGameRunningStatus(self):  # to be removed
        "return True if game has players that can make a move"

        if self.getTotalDiceCount() > 1:
            return True
        else:
            return False

    def setStartingPlayer(self, startingPlayer):
        "sets updates the order in which players are sequenced"

        playersList = [player for player in self.players]

        for key in playersList[playersList.index(startingPlayer):] + playersList[:playersList.index(startingPlayer)]:
            self.players[key] = self.players.pop(key)

    def hasAWinner(self):
        "Evaluates whether there is a winner in the game"

        activePlayers = 0
        for player in self.players:
            if self.players[player].remainingDice > 0:
                activePlayers += 1
        if activePlayers <= 1:
            return True
        else:
            return False

    def getWinner(self):
        if self.hasAWinner():
            print("{} wins in {} rounds".format(
                list(self.players.keys())[0], self.rounds))
            return list(self.players.keys())[0]

    def callBullshit(self, statement, caller):
        "Evaluates statement and removes dice accordingly. Returns liar who will start next round"

        allDice = list(itertools.chain(
            *[self.players[player].diceRolls for player in self.players]))
        players = [player for player in perudo.players]

        # Evaluating who is the liar
        if len([diceSide for diceSide in allDice if diceSide == statement[1]]) < statement[0]:
            liar = players[players.index(caller)-1]
        else:
            liar = caller

        # Removing dice and/or players
        if perudo.players[liar].remainingDice > 1:
            if self.params.gameLog:
                print("  Round Outcome: {} loses a dice".format(liar))
            perudo.players[liar].removeDice()
            nextStartingPlayer = liar
        else:
            if self.params.gameLog:
                print("  Round Outcome: {} exits the game".format(liar))
            perudo.players.pop(liar)
            nextStartingPlayer = players[players.index(liar)-1]

        return nextStartingPlayer

    def setPlayersDiceRolls(self):
        "Handles dice rolls for players"

        for player in self.players:
            self.players[player].setDiceRolls()
            if self.params.gameLog:
                print("    {} draws {}".format(
                    player, self.players[player].diceRolls))

    def runGameRound(self):
        "loops through a single round of the game, from dice roll to losing a die"

        if self.params.gameLog:
            print("  New Round Starts")
        self.setPlayersDiceRolls()
        roundIsRunning = True
        bids = []
        caller = ""
        self.rounds += 1

        #print("  Players Bids")
        while roundIsRunning is True and self.hasAWinner() is False:
            for player in [player for player in self.players if self.players[player].remainingDice >= 1]:
                legalMoves = []
                if len(self.getLegalBids(bids)) >= 1:
                    legalMoves.append("bid")
                if len(bids) >= 1:
                    legalMoves.append('bullshit')

                playerMove = choose(legalMoves)

                if playerMove == "bid":
                    bid = choose(self.getLegalBids(bids))
                    bids.append(bid)
                    if self.params.gameLog:
                        print("    {} bids {}".format(player, bid))

                if playerMove == "bullshit":
                    caller = player
                    roundIsRunning = False
                    if self.params.gameLog:
                        print("    {} calls BS".format(player))
                    break

        nextStartingPlayer = self.callBullshit(bids[-1], caller)
        self.setStartingPlayer(nextStartingPlayer)

    def startGame(self):
        "Game main loop which executes rounds until there is a winner"

        if self.params.gameLog:
            print("Game Init")
        while self.hasAWinner() == False:
            self.runGameRound()

        return self.getWinner()


# let's go
params = GameParameters()
perudo = PerudoEnv(params)

perudo.startGame()
