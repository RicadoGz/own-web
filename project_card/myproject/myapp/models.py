from django.db import models
from enum import Enum
import csv

class Suite(Enum):
    # suite.value is the 0123 suite.name was the SPADE
    SPADE = 0
    HEART = 1
    CLUB = 2
    DIAMOND = 3
# Create your models here.

class Card(models.Model):
    suite = models.IntegerField(choices=[(tag.value,tag.name) for tag in Suite])
    value = models.IntegerField()
    def __str__(self):
        suites = '♠♥♣♦'
        values = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return f'{suites[self.suite]}{values[self.value]}'
class Deck(models.Model):
    cards=models.ManyToManyField(Card)
    current = models.IntegerField(default=0)