from typing import List
from math import floor
from random import Random


class Deck:
    def __init__(self):
        self.cards: List[int] = []
        self.reset()
        
        
    def reset(self):
        self.cards = [i for i in range(12, 99) if i % 10 != 0]
        self.shuffle()

    def shuffle(self):
        for i in range(len(self.cards) - 1):
            j = Random().randint(0, i)

            element = self.cards[i]
            self.cards[i] = self.cards[j]
            self.cards[j] = element

    def pop(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)