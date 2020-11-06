from graphics import *
from random import randrange, choice
import json
import requests

"""
    Damage Calculator API: https://www.smogon.com/forums/threads/damage-calculator-api.3599759/
    Damage Calculator GitHub: https://github.com/smogon/damage-calc
    Damage Calculator Web App: https://calc.pokemonshowdown.com/
"""


def readPokeFile(filename):
    """ Name; Types; Abilities; Tier; HP; Attack; Defense; Special Attack; Special Defense; Speed; Next Evolution(s); Moves """
    infile = open(filename, "r")

    pokemonData = []
    header = []
    for line in infile:
        if line.startswith('Name;Types;'):
            line = line.strip()
            header = line.split(";")
            continue
        line = line.strip()
        lineList = line.split(";")
        currentPokemon = {}
        for i in range(len(header)):
            currentPokemon[header[i]] = lineList[i]
        currentPokemon['Moves'] = [x.strip()[1:-1] for x in currentPokemon['Moves'][1:-1].split(',')]
        currentPokemon['Abilities'] = [x.strip()[1:-1] for x in currentPokemon['Abilities'][1:-1].split(',')]
        pokemonData.append(currentPokemon)
    infile.close()
    return pokemonData

def readMoveFile():
    """Index; Name; Types; Category; Contest; PP; Power; Accuracy; Generation"""
    infile = open("move-data.csv", "r")

    Move2Animation = {}
    for line in infile:
        if line.startswith('Index,Name,'):
            continue
        line = line.strip()
        lineList = line.split(",")
        name = lineList[1]
        moveType = lineList[2]
        Move2Animation[name] = moveType
    return Move2Animation


if __name__ == '__main__':
    pokemonData = readPokeFile("pokemon-data.csv")
    moveData = readMoveFile()
