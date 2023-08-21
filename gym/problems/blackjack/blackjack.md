# Blackjack

## Background

Blackjack is one of the most popular casino card game in the world, which is also known as *Twenty-One*. Blackjack players do not compete against each other, they play agains the dealer. Cards $2$ through $10$ are worth their face value, and face cards (jack, queen, king) are also worth $10$, while an ace can either be $11$ or $1$ as your wish. Players are to reach highest value as long as it doesn't exceed $21$; a hand with value higher than $21$ is said to burst.

## Problem

The game is played with multiple decks, each of them contains standard 52 cards. At the beginning, the player is dealt two cards, and the dealer is dealt one card face up and one card face down. The player must decide whether to "hit" (draw another card) or "stand" (keep his current hand). The player can continue to hit until their exceeds $21$ or he choose to stand.

After the player has finished their turn, the dealer reveals their face-down card and must continue to hit until their hand value is 17 or higher. If the dealer's hand exceeds 21, they bust and the player wins. If the dealer's hand is higher than the player's hand and does not exceed 21, the player loses. If the player's hand is higher than the dealer's hand and does not exceed 21, the player wins. If the player and dealer have the same hand value, it is a tie (called a "push").


## Template

```python

class Solution:
    def setup(self, n_decks: int, player_hand: List[int], dealer_hand_face_up: int) -> None:
        """
        Called once before the start of the game.
        @param n_decks: number of decks, each deck contains standard 52 cards
        @param player_hand: the player's hand
        @param dealer_hand_face_up: the dealer's face-up card
        """
        raise NotImplementedError
    
    def take_action(self) -> str:
        """
        Called once per turn to allow the player to take an action.
        @return: "stand" or "hit"
        """
        raise NotImplementedError

    def on_feedback(self, new_card: int):
        """
        Called once per turn after the player takes an action.
        @param new_card: the new card drawn from the deck
        """
        raise NotImplementedError

```
