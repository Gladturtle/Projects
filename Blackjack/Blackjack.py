symbols = ["Hearts","Clubs","Diamonds","Spades"]
values = {"King":10,"Queen":10,"Jack":10,"Ace":11}
from random import random
from random import shuffle


class Card():
    def __init__(self,symbol,value):
        self.symbol = symbol
        self.value = value
        self.truevalue = value

    def __str__(self):
        return (f"This card is a {self.truevalue} of {self.symbol}")
    def card_value_set(self):
        if self.value.isdigit() == True:
            self.value = int(self.value)
        else:
            self.value = values[self.value]
class Deck():
    def __init__(self):
        self.thedeck = []
        for symbol in symbols:
            for num in range(2,11):
                new_card = Card(symbol,str(num))
                new_card.card_value_set()
                self.thedeck.append(new_card)
            for value in values:
                new_card = Card(symbol,value)
                new_card.card_value_set()
                self.thedeck.append(new_card)
    def __str__(self):
        printstr =""
        flag = False
        for cards in self.thedeck:
            if flag == True:
                printstr = printstr + " ,"+ str(cards)
            else:
                printstr = str(cards)
            flag = True    
        return printstr
    def shuffle_deck(self):
        shuffle(self.thedeck)
    def deal_card(self):
        try:
              return self.thedeck.pop()
        except:
            print("The deck is exhaused")
    def add_card(self,card):
        self.thedeck.append(card)
class Bank():
    def __init__(self,name):
        self.name = name
        self.bal = 10000
        self.bet = 0
    def withdraw_chips(self):
        amt = 0
        while amt !='n':
            while amt not in ['100','200','500','1000','2500','5000','10000','n'] :
                amt = input("Please enter the valuation of the chip you want to bet on the current game. Available chips are Rs.100, Rs.200, Rs.500, Rs.1000, Rs.2500, Rs.5000, Rs.10000. If you want to stop withdrawal, simply enter n  ")
                if amt not in ['100','200','500','1000','2500','5000','10000','n']:
                    print("Error!! Please select one of the available values!")
            if amt !='n':
                amt = int(amt)
            if amt!='n' and amt>self.bal:
                print('You are broke and do not have the money to bet this amt. Please choose a different amount or choose a different life path')
            elif amt!='n':
                print(f"Amount Rs.{amt} transacted")
                self.bal -=amt
                self.bet +=amt
    def money_correction(self,wingame):
        if wingame == 1:
            self.bal = self.bal + 2*self.bet
            self.bet = 0
        elif wingame == 0:
            self.bal = self.bal + self.bet
            self.bet = 0
        else:
            self.bet = 0
class Player():
    def __init__(self,name):
        self.name = name
        self.bankacc = Bank(name)
        self.hand = []
    def add_card(self,card):
        self.hand.append(card)
    def clear_hand(self):
        self.hand = []
    def withdraw_money(self):
        self.bankacc.withdraw_chips()
    def money_correction(self,wingame):
        self.bankacc.money_correction(wingame)
class Game():
    def __init__(self):
        name = input("What is your name?")
        self.player1 = Player(name)
        self.dealer = Player("Dealer")
        self.maindeck = Deck()
        self.maindeck.shuffle_deck()
    def print_cards(self):
        print("Cards of Player-------------------------------------")
        for card in self.player1.hand:
            print(card)
        print(f"The total value of the cards are {self.player1value}")
    def print_cards_dealer(self):
        print("Cards of Dealer-------------------------------------")
        for card in self.dealer.hand:
            print(card)
        print(f"The total value of the cards are {self.dealervalue}")
    def player_hand_value(self):
        for cards in self.player1.hand:
            self.player1value +=cards.value
        for card in self.player1.hand:
            if card.truevalue == "Ace" and self.player1value>21 :
                self.player1value -=10
    def dealer_hand_value(self):
        for cards in self.dealer.hand:
            self.dealervalue +=cards.value
        for card in self.dealer.hand:
            if card.truevalue == "Ace" and self.dealervalue>21:
                self.dealervalue -=10
    def double(self):
        if self.player1.bankacc.bet <= self.player1.bankacc.bal:
            self.player1.bankacc.bal = self.player1.bankacc.bal - self.player1.bankacc.bet
            self.player1.bankacc.bet = self.player1.bankacc.bet*2
            return 0 
        else:
            print("You brokie. Earn some money before betting")
            print("This will be considered as a hit and not a double")
            return -1
    def game(self):
        self.player1.withdraw_money()
        print(f"Bank Balance - {self.player1.bankacc.bal}")
        for num in range(0,2):
            self.player1.add_card(self.maindeck.deal_card())
            self.dealer.add_card(self.maindeck.deal_card())
        self.player1value = 0
        self.dealervalue = 0
        choice = ' '
        doubleornot = False
        while self.dealervalue<21 and self.player1value<21:
            self.dealer_hand_value()
            self.print_cards_dealer()
            self.player_hand_value()
            self.print_cards()
            self.player1value = 0
            self.dealervalue = 0
            if doubleornot == False:
                choice = input("Do you want to hit, pass or double?(Press h for hit, p for pass or d for double)")
            if choice =="h":
                self.player1.hand.append(self.maindeck.deal_card())
            if choice == "d":
                result = self.double()
                self.player1.hand.append(self.maindeck.deal_card())
                if result == 0:
                    choice = 'p'
                    doubleornot = True
            self.player_hand_value()
            self.print_cards()
            self.dealer_hand_value()
            if self.dealervalue <17:
                self.dealer.add_card(self.maindeck.deal_card())
            self.dealervalue = 0
            self.dealer_hand_value() 
            self.print_cards_dealer()
            if self.player1value >21 or (self.dealervalue>self.player1value and choice == 'p' and self.dealervalue>=17 and self.dealervalue<22) or self.dealervalue == 21:
                print("You have lost:(")
                self.player1.money_correction(-1)
                break
            elif self.dealervalue>21 or self.player1value == 21 or (self.dealervalue<self.player1value and self.dealervalue>=17):
                print("You have won!")
                self.player1.money_correction(1)
                break
            if self.dealervalue==self.player1value and self.dealervalue>=18 and choice == 'p':
                print("You have tied")
                self.player1.money_correction(0)
                break
            self.player1value = 0
            self.dealervalue = 0
    def reset(self):
        self.player1value = 0
        self.dealervalue = 0
        lenplayer1 = len(self.player1.hand)
        lendealer = len(self.dealer.hand)
        for card in range (0,lenplayer1):
            self.maindeck.add_card(self.player1.hand.pop())
        for card in range(0,lendealer) :
            self.maindeck.add_card(self.dealer.hand.pop())
        self.maindeck.shuffle_deck()
Game1 = Game()
gameon = True
while gameon:
    Game1.game()
    Game1.reset()
    gameon = input("Do you want to continue play?(Press y for yes and n for no)")
    if gameon == 'y':
        gameon = True
    elif gameon == 'n':
        gameon = False
    





    







