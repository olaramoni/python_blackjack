#Blackjack Command Line Game
#Dealer stands on 17 and above, blackjacks pay out 3:2
#Current state: Players start with 1000, can bet positive integer values smaller than their wallet value, deck made of 3 shuffled 52-card packs (Able to change in future)
               #Deals the card on top of deck one by one to players then dealer until all have two cards
               #If dealer gets a blackjack, other players with blackjacks get their original bet back, the rest lose theirs
               #Otherwise, players with blackjacks get 2.5* their original bet back to their wallet and skip their turn
               #Game rotates through player list, each player can either press A to hit(take card) or L to stand(continue to next player)
               #Player loses their original bet if they hit and the value of their hand goes above 21 (Aces are worth 1 or 11 depending on hand value)
               #Once all players are done, the dealer will either stand on hands worth more than 16, or hit until it reaches >16 / busts
               #At the end of the round, players with greater hands than the dealer receive 2* their original bet back to their wallet
                                        #players with equal hands to the dealer get their original bet back and players below lose their original bet
               #The game repeats until all players run out of money(Untested) or the maximum number of rounds is reached(default 3 currently)
#Deck should refill and reshuffle once below 50 cards left, haven't tested yet so unsure if it works
#Missing functions/rules: Double down, Split, Insurance, User input validation(Exception handling), GUI(Long term)


#import pygame
import random
import os
import sys
import time
import subprocess
try:
    import keyboard
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "keyboard"])
    import keyboard

if sys.version_info < (3, 10):
    print("Blackjack.py requires Python 3.10 or higher to run. Your current version is {}.".format(sys.version))
    sys.exit(1)

#if platform.system() == 'Windows':
    #os.environ['SDL_VIDEODRIVER'] = 'windib'

class player:
    def __init__(self, name:str, wallet=1000, current_stake=0, still_in_game=True):
        self.name = name
        self.wallet = wallet
        self.hand = []
        self.current_stake = current_stake
        self.still_in_game = still_in_game

    def give_card(self, card):
        time.sleep(0.3)
        card.owner = self.name
        self.hand.append(card)
    
    def is_blackjack(self):
            match self.hand[0].value:
                case 11:
                    if self.hand[1].value == 10:
                        time.sleep(0.5)
                        return True
                    else:
                        return False
                case 10:
                    if self.hand[1].value == 11:
                        time.sleep(0.5)
                        return True
                    else:
                        return False
                case _:
                    return False
        

    def get_hand_value(self):
        sum = 0
        for cards in self.hand:
            sum += cards.value
        if sum > 21:
            for cards in self.hand:
                if cards.value == 11:
                    sum -= 10
                    if sum < 22:
                        break             
        return sum
    
    def is_bust(self):
        sum = self.get_hand_value()
        if sum > 21:
            return True
        else:
            return False

                
    
    def __str__(self):
        return "Player 1: £{}\nCards Held: {}".format(wallet, hand)

class card:
    def __init__(self, suit:str, name:str, value:int):
        self.suit = suit
        self.name = name
        self.value = value
        self.owner = None
    
    def __str__(self):
        return "{} of {}".format(self.name, self.suit)
    
    def value(self):
        return self.value

class deck:
    def __init__(self, packs_used:int):
        self.packs_used = packs_used
        self.cards_in_play = []
        self.used_pile = []
    
    def __str__(self):
        #return "{} cards in play, {} in discard pile".format(len(self.cards_in_play), len(self.used_pile))
        cards = []
        for card in self.cards_in_play:
            cards.append(card)
        return str(cards)

    
    def populate_deck(self):
        for i in range(0, self.packs_used):
            for i in range(0,4):
                if i == 0: #♡
                    self.cards_in_play.append(card(suit="♡", value=11, name='Ace'))
                    for i in range(2,11):
                        self.cards_in_play.append(card(suit="♡", value=i, name = str(i)))
                    self.cards_in_play.append(card(suit="♡", value=10, name='Jack'))
                    self.cards_in_play.append(card(suit="♡", value=10, name='Queen'))
                    self.cards_in_play.append(card(suit="♡", value=10, name='King'))

                if i == 1: #♢
                    self.cards_in_play.append(card(suit="♢", value=11, name='Ace'))
                    for i in range(2,11):
                        self.cards_in_play.append(card(suit="♢", value=i, name = str(i)))
                    self.cards_in_play.append(card(suit="♢", value=10, name='Jack'))
                    self.cards_in_play.append(card(suit="♢", value=10, name='Queen'))
                    self.cards_in_play.append(card(suit="♢", value=10, name='King'))

                if i == 2: #♧
                    self.cards_in_play.append(card(suit="♧", value=11, name='Ace'))
                    for i in range(2,11):
                        self.cards_in_play.append(card(suit="♧", value=i, name = str(i)))
                    self.cards_in_play.append(card(suit="♧", value=10, name='Jack'))
                    self.cards_in_play.append(card(suit="♧", value=10, name='Queen'))
                    self.cards_in_play.append(card(suit="♧", value=10, name='King'))

                if i == 3: #♤
                    self.cards_in_play.append(card(suit="♤", value=11, name='Ace'))
                    for i in range(2,11):
                        self.cards_in_play.append(card(suit="♤", value=i, name = str(i)))
                    self.cards_in_play.append(card(suit="♤", value=10, name='Jack'))
                    self.cards_in_play.append(card(suit="♤", value=10, name='Queen'))
                    self.cards_in_play.append(card(suit="♤", value=10, name='King'))
        
        random.shuffle(self.cards_in_play) #shuffle deck
        print("------------------------------------------------\nDeck generated and shuffled")
        #print("{} cards in the deck".format(len(self.cards_in_play)))

    def take_card(self):
        print(self.cards_in_play[0])
        self.used_pile.append(self.cards_in_play[0])
        return self.cards_in_play.pop(0)

class Game:
    def __init__(self, player_list:list, max_rounds:int, dealer=player('Dealer', 0), gameDeck=deck(3)):
        self.player_list = player_list
        self.dealer = dealer
        self.gameDeck = gameDeck
        self.max_rounds = max_rounds

    def get_players(self):
        return self.player_list

    def round_end(self):
        print("Distributing winnings and resetting round\nCURRENT STANDINGS:")
        for player in self.player_list:
            if player.is_blackjack():
                if self.dealer.is_blackjack():
                    player.wallet += player.current_stake
                    print("{} pushes, £{} left in wallet".format(player.name, player.wallet))
                    continue
                else:
                    player.wallet += player.current_stake*2.5
                    print("{} wins £{}, £{} left in wallet".format(player.name, player.current_stake*1.5, player.wallet))
                    continue
            else:
                if player.is_bust():
                    print("{} loses £{}, £{} left in wallet".format(player.name, player.current_stake, player.wallet))
                else:
                    if self.dealer.is_bust():
                        player.wallet += player.current_stake*2
                        print("{} wins £{}, £{} in wallet".format(player.name, player.current_stake, player.wallet))
                    else:
                        if player.get_hand_value() > self.dealer.get_hand_value():
                            player.wallet += player.current_stake*2
                            print("{} wins £{}, £{} in wallet".format(player.name, player.current_stake, player.wallet))
                        elif player.get_hand_value() == self.dealer.get_hand_value():
                            player.wallet += player.current_stake
                            print("{} pushes, £{} left in wallet".format(player.name, player.wallet))
                        else:
                            print("{} loses £{}, £{} left in wallet".format(player.name, player.current_stake, player.wallet))
            if player.wallet == 0 and not player.is_blackjack():
                print("{} is bankrupt, removing from game".format(player.name))
                player.still_in_game = False
            player.hand = []
            player.current_stake = 0
        self.dealer.hand = []
        self.player_list = [player for player in self.player_list if player.still_in_game] #Reestablish playerlist without bankrupt players
        time.sleep(1.5)
        

    def game_round(self):
        roundStart = True
        while roundStart == True:
            print("Taking bets")
            for player in self.player_list:
                #player.current_stake = 50
                #player.wallet -= player.current_stake
                while player.current_stake == 0 or player.current_stake > player.wallet:
                    player.current_stake = int(input("{}, £{} left in wallet, place your bet: ".format(player.name, player.wallet)))
                player.wallet -= player.current_stake
            print("Betting closed \nRound starting, dealing cards\n--------------------------------------")
            for i in range(0,2):
                for player in self.player_list:
                    player.give_card(self.gameDeck.cards_in_play[0])
                    del self.gameDeck.cards_in_play[0]
                    print(player.hand[-1], "drawn to ", player.name)
                self.dealer.give_card(self.gameDeck.cards_in_play[0])
                del self.gameDeck.cards_in_play[0]
                print(self.dealer.hand[-1], "drawn to ", self.dealer.name)
            time.sleep(1)
            print("--------------------------------------")
            print(self.dealer.hand[0],', ',  self.dealer.hand[1], ", Dealer hand value: ", (self.dealer.get_hand_value()))
            if self.dealer.is_blackjack():
                print("House blackjack!\n {}, {}".format(self.dealer.hand[0], self.dealer.hand[1]))
                self.round_end()
                roundStart = False
                return

            for player in self.player_list:
                print("--------------------------------------")
                print("PRESS A TO HIT OR L TO STAND")
                print(player.name,'|',player.hand[0], ", ", player.hand[1], "| Hand value: ", (player.hand[0].value + player.hand[1].value))
                
                if player.is_blackjack():
                    print("{} blackjack! £{} won".format(player.name, player.current_stake*1.5))
                    #player.wallet += (player.current_stake*2.5)
                    #player.current_stake = 0
                    continue
                else:
                    while True:
                        keyboard.read_key()
                        if keyboard.is_pressed("A"):
                            time.sleep(0.2)
                            player.give_card(self.gameDeck.take_card())
                            print("{}'s current hand value: {}".format(player.name, player.get_hand_value()))
                            if player.is_bust():
                                print("Player Bust")
                                time.sleep(1)
                                #player.current_stake = 0
                                break
                            elif player.get_hand_value == 21:
                                print("{} stands on 21")
                                time.sleep(1)
                                break
                        if keyboard.is_pressed("L"):
                            print("{} stands on {}".format(player.name, player.get_hand_value()))
                            break
            time.sleep(0.3)
            players_left = 0
            for player in self.player_list:
                if player.current_stake != 0:
                    players_left += 1
            
            if players_left == 0:
                print("House wins!")
                self.round_end
                roundStart = False
                return 
                
            print("--------------------------------------")
            print("Dealer in play")
            time.sleep(1)
            print(self.dealer.hand[0], ", ", self.dealer.hand[1], "| Dealer hand value: ", self.dealer.get_hand_value())
            all_players_bust = True
            while not all_players_bust:
                for player in self.player_list:
                    if not player.is_bust():
                        all_players_bust = False
                print("All players bust, ending round")
                self.round_end()
                roundStart = False
                return
                    
            while self.dealer.get_hand_value() < 17:
                time.sleep(0.3)
                self.dealer.give_card(self.gameDeck.take_card())
                print("Dealer hand value: {}".format(self.dealer.get_hand_value()))
                if self.dealer.is_bust():
                    print("Dealer busts")
                    print("--------------------------------------")
                    time.sleep(1)
                    self.round_end()
                    roundStart = False
                    return
            print("Dealer stands on ", self.dealer.get_hand_value())
            print("--------------------------------------")
            time.sleep(1)
            #for player in self.player_list:
                #if player.get_hand_value() < self.dealer.get_hand_value() and not self.dealer.is_bust():
                    #player.current_stake = 0
            self.round_end()
            roundStart = False
            return
        return
                        
        #return (self.player_list[0].hand)



def main():
    #user1 = player('Player1')
    #user2 = player('Player2')
    #user3 = player('Player3')
    #user4 = player('Player4')
    users = []
    player_count = int(input("Enter number of players: "))
    for i in range(0, player_count):
        users.append(player(input("Enter player name: ")))
    max_rounds = int(input("Set a maximum amount of hands to play: "))

    game = Game(users, max_rounds=max_rounds)
    game.gameDeck.populate_deck()
    print("STARTING GAME")
    for i in range(0, game.max_rounds):
        print("------------------------------------------------\nRound ", i+1)
        if len(game.gameDeck.cards_in_play) < 50:
            game.gameDeck.cards_in_play = []
            game.gameDeck.used_pile = []
            game.gameDeck.populate_deck()      
        if not game.get_players():
            print("No players remaining, exiting game")
            break
        game.game_round()
    print("------------------------------------------------\nFinal standings:")
    for players in game.get_players():
        print("{} | £{}".format(players.name, players.wallet))


if __name__ == '__main__':
    main()