# Sofia Fall
# Wed Nov 16
# Blackjack Game

# Import libraries
import os
import random
import sys
import time


class Card:
    """ This class represents a card with a rank and a suit with methods to
    build the card image and returns the symbol corresponding to a suit. """

    def __init__(self, rank, suit):
        """ Class constructor of the Card class that constructs an object with the
        provided rank and suit. """

        self.rank = rank
        self.suit = suit

    def __str__(self):
        """ This string method prints Card as a string. """

        return self.rank + ' of ' + self.suit

    def build(self):
        """ Overloaded method, same name different parameters ."""

        return self.build(self, False)

    def build(self, hidden):
        """ This method to build a Card with a boulean variable that specifies whether the
        Card is hidden or not (flag). """

        array = []  # Create an empty array
        array.append('┌─────────┐')  # Put top line of Card

        # Build Card if flag is true
        if hidden is True:
            array.append('|  * * *  |')
            array.append('| *     * |')
            array.append('|       * |')
            array.append('|     *   |')
            array.append('|    *    |')
            array.append('|         |')
            array.append('|    *    |')

        # Build Card if flag is false
        else:
            array.append('│ {:<2}      │'.format(self.rank))
            array.append('│         │')
            array.append('│         │')
            array.append('│    {}    │'.format(self.symbolize()[0]))
            array.append('│         │')
            array.append('│         │')
            array.append('│      {:>2} │'.format(self.rank))

        array.append('└─────────┘')  # Put Bottom line of Card
        return array

    def symbolize(self):
        """ Returns a symbol for the suit of Card as a character """

        match self.suit:
            case 'CLUBS':
                return '\u2667',  # White Club Suit
            case 'DIAMONDS':
                return '\u2662',  # White Diamond Suit
            case 'HEARTS':
                return '\u2661',  # White Heart Suit
            case 'SPADES':
                return '\u2664',  # White Spade Suit


class Deck:
    """ This class represents a deck of 52 cards. """

    __deck_cards__ = 52
    __ranks__ = ['A', '2', '3', '4', '5', '6',
                 '7', '8', '9', '10', 'J', 'Q', 'K']
    __suits__ = ['CLUBS', 'DIAMONDS', 'HEARTS', 'SPADES']

    def __init__(self):
        """ Class constructor """
        self.deck = Deck.__build__()

    def __build__():
        """ Builds a deck of Cards using nested for loops,
        then randomly shuffles the array. """

        deck = []
        for rank in Deck.__ranks__:
            for suit in Deck.__suits__:
                deck.append(Card(rank, suit))
        random.shuffle(deck)
        return deck

    def __str__(self):
        """ Builds a deck of Cards using a nested for loop,
        then randomly shuffles the array. """

        cards = ''
        for card in self.deck:
            if card is not None:
                cards += str(card) + '\n'
        cards = cards.rstrip(cards[-1])  # Strip the trailing new line char
        return cards

    def __len__(self):
        """ Returns the length of the deck array as an integer. """

        return len(self.deck)

    def draw_card(self):
        """ Remove a Card from the top of the deck. """

        return self.deck.pop()


class Player:
    """ This class describes a player with a name, a hand, a score, and
    a dealer status. """

    def __init__(self, name, dealer):
        """ Class constructor of the Player class """
        self.name = name
        self.hand = []
        self.score = 0
        self.dealer = dealer

    def pull_n_cards(self, n, deck):
        """ Pull and return n amount of Cards from the deck. """
        for num in range(n):
            if deck:
                self.hand.append(deck.draw_card())
        return self

    def __prepare__(self):
        """ Prepares the cards to be displayed in the terminal with a specified number of
        cards per row. """

        # A constant for the number of cards per row.
        _NUMBER_OF_CARDS_PER_ROW = 4
        array = []

        # Split larger arrays into groups of _NUMBER_OF_CARDS_PER_ROW.
        temp = []
        index = 0

        for card in self.hand:  # For each card in hand
            if index < _NUMBER_OF_CARDS_PER_ROW:  # If index < 4
                temp.append(card)  # Append card to temp array
                index = index + 1  # Increment index by 1
            else:  # If index = 4
                array.append(temp)  # Append temp to array
                temp = []  # Reset temp array
                index = 0  # Reset index counter

        array.append(temp)

        return array

    def show_hand(self, hidden):
        """ Process the groups of hands returned by the prepare method to reflect
        dealer or player status, and print to console as a string. """

        # Determine the number of lines per Card
        _NUMBER_OF_LINES_PER_CARD = 9

        # Generate the groups from player's hand using the prepare method
        groups = self.__prepare__()
        temp = groups[0][0]  # Create a temp array

        # For each group in groups
        for group in groups:
            array = []  # Creates an empty array

            # For each card in group
            for card in group:
                array.append(card.build(hidden))  # Append Card to array
                if card == temp and hidden:  # If the card is in the array
                    array.pop()
                    # If it's the last card, pop it, append it, and move on
                    array.append(card.build(not hidden))

            # Store the length of the array in a variable
            num_of_cards = len(array)

            # Itterate through the array and print
            for line in range(_NUMBER_OF_LINES_PER_CARD):
                str = ''
                for card in range(num_of_cards):
                    str = str + array[card][line]

                print(str)

    def evaluate_hand(self):
        """ Evaluate and return the score. """

        # Ranks dictionary with key value pairs
        ranks = {
            'A': 11,
            'J': 10,
            'Q': 10,
            'K': 10
        }

        score = 0  # Track the score
        number_of_aces = 0  # Number of Aces

        # Logic to evaluate the socre of a hand
        for card in self.hand:
            if card.rank in ranks.keys():
                score = score + int(ranks.get(card.rank))
                if card.rank == 'A':
                    number_of_aces = number_of_aces + 1
            else:
                score = score + int(card.rank)

            while number_of_aces > 0 and score > 21:
                score = score - 10
                number_of_aces = number_of_aces - 1

        return score  # return score to call method


def clear():
    """ Clear terminal. """

    os.system('clear')


def show_rules():
    """ Ask player if they know how to play. Provide link with rules attached. """
    clear()
    print('\n\nHere are the rules of blackjack: http://en.wikipedia.org/wiki/Blackjack')
    input("\n\nPress Enter to continue... ")


def determine_winner(player_score, dealer_score):
    """ Print game outcome from 4 possible situations."""

    # Player wins if dealer > 21
    if dealer_score > 21:
        print('Dealer busts. Player wins.')
    # Player loses if player > 21 or if player < dealer
    elif player_score > 21 or player_score < dealer_score:
        print('Player loses.')
    # Player wins if player > dealer
    elif player_score > dealer_score:
        print('Player wins.')
    # In the event of a tie
    else:
        print('Tie.')


def sp1(str, duration):
    """ Special method to display Loading"""

    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(duration)
    print()


if __name__ == '__main__':
    """Main method"""

    sp1("Loading", 1)

    sp1("Welcome to Sofia's blackjack game. Please wait while the game loads!...\nEnjoy!", 0)

    input("Press ENTER to continue\n>>>  ")

    clear()

    # Choice dictionaries and experienced status
    yes = {'YES', 'Y'}
    no = {'NO', 'N'}
    experienced = False

    print('Have you ever played Blackjack before?')
    print('Please respond with yes or no.')

    while not experienced:
        choice = input().upper()
        if choice in yes:
            experienced = True
        elif choice in no:
            show_rules()
            experienced = True
        else:
            print("Please respond with yes or no.")

    # Game turn
    playing = True
    while playing:

        # Begin the game
        clear()
        print("Great, let's play!")

        # Create and shuffle a new deck of cards
        deck = Deck()

        # Create a dealer
        dealer = Player('Dealer', True)

        #  Create a player
        player = Player('Player', False)
        name = input('What is your name? ')
        if name:
            player.name = name

        # Deal two cards to each player
        player.pull_n_cards(2, deck)
        dealer.pull_n_cards(2, deck)

        # Player turn flag
        player_turn = True
        print(f"\nHi {player.name}! Your turn begins now...\n\n")

        # Player turn
        while player_turn:

            # Display player hand
            player.show_hand(False)

            # Evaluate the hand
            player.score = player.evaluate_hand()
            print(player.score)

            # End player turn if score is greater than 21
            if player.score > 21:
                player_turn = False
                break

            # Choice dictionaries and experienced status
            hit = {'HIT', 'H'}
            stand = {'STAND', 'S'}
            decided = False

            while not decided:
                # Prompt the player for a move
                move = input('\n\nEnter H to HIT or S to STAND: ').upper()

                # If player decided to hit
                if move in hit:
                    print('\n\nYou hit!')

                    player.pull_n_cards(1, deck)
                    player.score = player.evaluate_hand()
                    player.show_hand(False)
                    print(player.score)

                    if player.score > 21:
                        decided = True
                        player_turn = False

                # If player decides to stand
                elif move in stand:
                    print('\n\nYou stand!')
                    decided = True
                    player_turn = False

                # If player enters an invalid option
                else:
                    print("\n\nPlease respond with H to HIT or S to STAND.")

        print('\n\nPlayer turn finished.\n\n')

        # Dealer turn
        dealer_turn = True
        print('\n\nDealer turn begins now...\n\n')
        input('Press enter to continue... ')

        # Player turn
        while dealer_turn:
            # Display player hand
            dealer.show_hand(True)

            # Evaluate the hand
            dealer.score = dealer.evaluate_hand()
            print(dealer.score)

            # End dealer turn if score is less than 17
            while dealer.score < 17:
                dealer.pull_n_cards(1, deck)
                dealer.score = dealer.evaluate_hand()
                dealer.show_hand(True)
                print(dealer.score)
                input('Press enter to continue... ')

                if dealer.score > 21:
                    dealer_turn = False
                    break

            dealer_turn = False

        """Clear the screen and display both hands"""

        print('\n\nShowing both hands...\n\n')
        print('Player')
        player.show_hand(False)
        print(player.score)

        print('Dealer')
        dealer.show_hand(False)
        print(dealer.score)

        """Determine a winner"""
        determine_winner(player.score, dealer.score)

        """Continue?"""
        print('\nNew game? Please respond with yes or no.')

        """Choice dictionaries and experienced status"""
        yes = {'YES', 'Y'}
        no = {'NO', 'N'}

        while playing:
            choice = input().upper()
            if choice in yes:
                playing = True
                break
            elif choice in no:
                playing = False
            else:
                print("Please respond with yes or no.")