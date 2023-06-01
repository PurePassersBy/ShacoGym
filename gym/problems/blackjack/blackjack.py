import time
from typing import Any, List, Optional

import numpy as np

from ..base import Environment


class Blackjack(Environment):
    REWARDS: List[int] = []

    def __init__(self, seed: Optional[int], n_decks: int) -> None:
        self.n_decks = n_decks
        if seed is None:
            seed = int(time.time())
        self.rng = np.random.default_rng(seed)
        
    def setup(self):
        self.cards: List[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * self.n_decks
        self.rng.shuffle(self.cards)
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]

        return {'n_decks': self.n_decks, 'player_hand': self.player_hand, 'dealer_hand_face_up': self.dealer_hand[0]}

    def run(self, sol):
        self.final_status = 'none'
        while True:
            action = sol.take_action()
            is_done = self.on_action(action)
            if is_done:
                break
            new_card = self.draw_card()
            sol.on_feedback(new_card)
            
        if self.final_status == 'none':
            while self.get_hand_value(self.dealer_hand) < 17:
                self.dealer_hand.append(self.draw_card())
            if self.get_hand_value(self.dealer_hand) > 21:
                self.final_status = 'win'
            elif self.get_hand_value(self.dealer_hand) > self.get_hand_value(self.player_hand):
                self.final_status = 'lose'
            elif self.get_hand_value(self.dealer_hand) < self.get_hand_value(self.player_hand):
                self.final_status = 'win'
            else:
                self.final_status = 'draw'

        self.logger.info(f'You got {self.final_status} with {self.get_hand_value(self.player_hand)} score, while dealer with {self.get_hand_value(self.dealer_hand)} score.')
        self.REWARDS.append(1 if self.final_status == 'win' else 0 if self.final_status == 'draw' else -1)

    def on_action(self, action: str) -> bool:
        if action == 'stand':
            return True
        elif action == 'hit':
            self.player_hand.append(self.draw_card())
            if self.get_hand_value(self.player_hand) > 21:
                self.final_status = 'lose'
                return True
            return False
        else:
            raise ValueError(f'Invalid action {action}, must be "stand" or "hit"')

    def draw_card(self) -> int:
        return self.cards.pop()
    
    def get_hand_value(self, hand: List[int]) -> int:
        value = sum(hand)
        if value > 21 and 11 in hand:
            value -= 10
        return value

    @classmethod
    def show_results(cls):
        print('\nYour results:')
        n_wins = sum(1 for r in cls.REWARDS if r == 1)
        n_loses = sum(1 for r in cls.REWARDS if r == -1)
        n_draws = sum(1 for r in cls.REWARDS if r == 0)
        print(f'Win: {n_wins}, Lose: {n_loses}, Draw: {n_draws}, Final score: {n_wins - n_loses}')

    @classmethod
    def from_play_mode(cls) -> "Blackjack":
        raise NotImplementedError

    @classmethod
    def get_interactive_player(cls):
        raise NotImplementedError
