from random import shuffle
from time import sleep

#Create our classes: deck, hand, user

class deck:
    suits = ['c', 'd', 'h', 's']
    values = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    cards = []

    def resetdeck(self):
        self.cards = []
        for j in self.values:
            for i in self.suits:
                self.cards.append(str(j) + i)
    
    def shuffle(self):
        shuffle(self.cards)
    
    def deal(self, dealee):
        newCard = self.cards.pop()
        dealee.hand.append(newCard)
        if newCard[0] == '1' or newCard[0] == 'J'  or newCard[0] == 'Q' or newCard[0] == 'K':
            dealee.score += 10
        elif newCard[0] == 'A':
            if dealee.score >= 11:
                dealee.score += 1
            else:
                dealee.aces += 1
                dealee.score += 11
        else:
            dealee.score += int(newCard[0])          

class hand:
    hand = []
    score = 0
    aces = 0

    def resethand(self):
        self.hand = []
        self.score = 0

class user(hand):
    money = 10
    betSize = 0
    def checkMoney(self):
        if self.money == 0:
                print("You have no more money. Game over\n")
                playAgain = input("Enter 'y' to play again or any other key to quit:\n")
                sleep(0.5)
                if playAgain == 'y':
                    self.money += 10
                    print("\nStarting new game...")
                    sleep(0.5)
                    newGame()
                else:
                    quit()

#Create our class instances (objects)
comp = hand()
player = user()
gameDeck = deck()

#Create the functions which will run our game

def printPlayerCards():
    print("\nYour cards: " + str(player.hand))
    print("Your score: " + str(player.score) + '\n')

def printAllCards():
    print("\nYour cards: " + str(player.hand))
    print('Your score: ' + str(player.score))
    print("\nComputer cards: " + str(comp.hand))
    print('Computer score: ' + str(comp.score) + '\n')

def playerWins():
    printAllCards()
    print("You win!\n")
    player.money += player.betSize
    with open("blackjackmoney.txt", 'w') as file:
        file.write(str(player.money))

def playerLoses():
    print("You lose!\n")
    player.money -= player.betSize
    with open("blackjackmoney.txt", 'w') as file:
        file.write(str(player.money))
    player.checkMoney()

def newGame():
    player.resethand()
    comp.resethand()
    gameDeck.resetdeck()
    gameDeck.shuffle()
    gameDeck.deal(comp)
    gameDeck.deal(player)
    gameDeck.deal(comp)
    gameDeck.deal(player)

    print('\nYou have £' + str(player.money) + '\n')

    player.betSize = int(input('Bet size: £'))

    while player.betSize <= 0 or player.betSize > player.money:
        player.betSize = int(input('Bet size: £'))

    sleep(0.5)
    printPlayerCards()

    if player.score == 21:
        printAllCards()
        print("You win!\n")
        player.money += player.betSize
        with open("blackjackmoney.txt", 'w') as file:
            file.write(str(player.money))

def hit():
    gameDeck.deal(player)
    sleep(0.5)
    if player.score > 21:
        if player.aces > 0:
            player.score -= 10
            player.aces -= 1
            printPlayerCards()
        else:
            printPlayerCards()
            playerLoses()
    else:
        printPlayerCards()

def stand():
    sleep(0.5)
    while comp.score < 18 or comp.score < player.score:
        gameDeck.deal(comp)
    if comp.score > 21:
        if comp.aces > 0:
            comp.score -= 10
            comp.aces -= 1
        else:
            printAllCards()
            playerWins()
    elif comp.score > player.score:
        printAllCards()
        playerLoses()
    elif comp.score == player.score:
        printAllCards()
        print("Draw!\n")
    else:
        printAllCards()
        playerWins()

#The game starts here:
#Check if the user wants to load the amount of chips present when last playing
with open("blackjackmoney.txt") as file:
    amountSaved = file.readline()
if int(amountSaved) and int(amountSaved) > 0:
    print("\nYou have £" + str(amountSaved) + " saved from a previous game.")
    ans = input("Press 'y' to continue with saved money or another key to restart:\n")
    if ans == 'y':
        player.money = int(amountSaved)

#Game logic
newGame()
while player.score <= 21:
    answer = input("Press 'h' to hit or 's' to stand \n")
    if answer == 'h':
        hit() 
    elif answer == 's':
        stand()
        newGame()