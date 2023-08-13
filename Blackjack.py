import random
import time

# Function to calculate the score of a hand
def calculate_score(hand):
    score = 0
    num_aces = 0
    for card in hand:
        rank = card.split(" of ")[0]
        if rank in ["Jack", "Queen", "King"]:
            score += 10
        elif rank == "Ace":
            score += 11
            num_aces += 1
        else:
            score += int(rank)

    # Deduct 10 for each Ace if score is over 21
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1

    return score

def print_letter_by_letter(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.09)
    print()

# Define the deck of cards
suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
# Multiple at the end is the amount of decks in play
deck = [rank + " of " + suit for suit in suits for rank in ranks] * 6

# Shuffle the deck once
random.shuffle(deck)
#burn top card
deck.pop()
print("A card was burned and the deck has began.")

count = 0
deck_count = 0
player_balance = 200
while deck:
    # Display player's balance
    print("Your balance is:", player_balance)
    print("Deck count:", deck_count)
    
    # Ask player for the bet
    bet = int(input("How much do you want to bet? "))
    if bet > player_balance:
        print("You don't have enough money to place that bet.")
        break
    
    # Deal two cards to the player and two cards to the dealer
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # Update the deck count
    for card in player_hand + dealer_hand:
        rank = card.split(" of ")[0]
        if rank in ["2", "3", "4", "5", "6"]:
            deck_count += 1
        elif rank in ["10", "Jack", "Queen", "King"]:
            deck_count -= 1

    # Display dealer's cards
    print("Dealer's current hand is:", dealer_hand[0], "and [hidden]")

    # Player turn
    player_score = calculate_score(player_hand)
    print("Your current hand is:", player_hand)
    print("Your current score is:", player_score)

    # Check if player has two of the same cards
    if player_hand[0][0] == player_hand[1][0]:
      split = input("Do you want to split? (y/n) ")
      if split.lower() == "y":
        print("Your bet has been doubled.")
        bet = 2 * bet
        hand_1 = [player_hand[0]]
        hand_2 = [player_hand[1]]
        print(f"Your first hand is {hand_1}")
        print(f"Your second hand is {hand_2}")
        while True:
            action_1 = input("First hand. Do you want to hit or stand? (h/s)")
            if action_1.lower() == "h":
                hand_1.append(deck.pop())
                print(f"Your first hand is {hand_1}")
                print(f"Your first score is {calculate_score(hand_1)}")
            elif action_1.lower() != "h":
                break
            if calculate_score(hand_1) > 21:
                print("Bust!")
                break
        while True:
            action_2 = input("Second hand. Do you want to hit or stand? (h/s)")
            if action_2.lower() == "h":
                hand_2.append(deck.pop())
                print(f"Your second hand is {hand_2}")
                print(f"Your second score is {calculate_score(hand_2)}")
            elif action_2.lower() != "h":
                break
            if calculate_score(hand_2) > 21:
                print("Bust!")
                break
        if calculate_score(hand_1) > 21 and calculate_score(hand_2) > 21:
            break
    else:
        if player_score > 11:
            while player_score < 21:
                action = input("Do you want to hit or stand? (h/s)")
                if action == "h":
                    player_hand.append(deck.pop())
                    player_score = calculate_score(player_hand)
                    print("Your current hand is:", player_hand)
                    print("Your current score is:", player_score)
                else:
                    break
        else:
            double_down = input("Do you want to double down? (y/n) ")
            if double_down == "y":
                player_hand.append(deck.pop())
                player_score = calculate_score(player_hand)
                print("Your current hand is:", player_hand)
                print("Your current score is:", player_score)
            else:
                while player_score < 21:
                    action = input("Do you want to hit or stand? (h/s)")
                    if action == "h":
                        player_hand.append(deck.pop())
                        player_score = calculate_score(player_hand)
                        print("Your current hand is:", player_hand)
                        print("Your current score is:", player_score)
                    else:
                        break

    # Dealer turn
    dealer_score = calculate_score(dealer_hand)
    print(f"Dealer's hand is now: {dealer_hand[0]} and ", end='')
    print_letter_by_letter(dealer_hand[1])

    if player_score <= 21:
        while dealer_score < 17:
            next_card = deck.pop()
            dealer_hand.append(next_card)
            dealer_score = calculate_score(dealer_hand)
            print(f"Dealer draws: {next_card}")
            print(f"Dealer's hand is now: {dealer_hand}")
            time.sleep(1)
    
    # Determine the winner
    if player_score > 21:
        print("You bust. You lose.")
        player_balance -= bet
    elif dealer_score > 21:
        print("Dealer busts. You win!")
        player_balance += 2 * bet
    elif player_score > dealer_score:
        print("You win!")
        player_balance += 2 * bet
    elif dealer_score > player_score:
        print("You lose.")
        player_balance -= bet
    else:
        print("It's a tie.")
        player_balance = player_balance


print("Your balance is:", player_balance)
