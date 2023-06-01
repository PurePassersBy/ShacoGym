from typing import List


class Solution:
    def setup(self, n_decks: int, player_hand: List[int], dealer_hand_face_up: int) -> None:
        """
        Called once before the start of the game.
        @param n_decks: number of decks, each deck contains standard 52 cards
        @param player_hand: the player's hand
        @param dealer_hand_face_up: the dealer's face-up card
        """
        self.n_decks = n_decks
        self.player_hand = player_hand
        self.dealer_hand_face_up = dealer_hand_face_up
    
    def take_action(self) -> str:
        """
        Called once per turn to allow the player to take an action.
        @return: "stand" or "hit"
        """
        if self.get_hand_value() >= 17:
            return 'stand'
        else:
            return 'hit'

    def get_hand_value(self) -> int:
        """
        @param hand: the hand to calculate the value of
        @return: the value of the hand
        """
        value = sum(self.player_hand)
        if value > 21 and 11 in self.player_hand:
            value -= 10
        return value

    def on_feedback(self, new_card: int):
        """
        Called once per turn after the player takes an action.
        @param new_card: the new card drawn from the deck
        """
        self.player_hand.append(new_card)
