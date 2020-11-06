from graphics import *
from tkinter.messagebox import showinfo
from move import readPokeFile, readMoveFile
from resizeImageZelle import resizeAndDisplayImage
from time import sleep
import random
import requests

def calculateDamage(attackingPokemon, defendingPokemon, moveUsed):
    """
        Description: Calculates damage a Pokemon's move does to another Pokemon
        Parameters: attackingPokemon- the attacking Pokemon's stats (dict),
                    defendingPokemon- the defending Pokemon's stats (dict),
                    moveUsed- the move used (str)
        Return Value: damage the move deals to the opposing Pokemon (int)

        Damage Calculator API: https://www.smogon.com/forums/threads/damage-calculator-api.3599759/
        Damage Calculator GitHub: https://github.com/smogon/damage-calc
        Damage Calculator Web App: https://calc.pokemonshowdown.com/
    """

    # POST method API request -- need to convert to python syntax
    url = 'https://calc-api.herokuapp.com/calc-api'

    # Both attacker and defender object should look something like this:
    attackerPokemonStats = {
        # species name AS IT IS IN THE POKEDEX [REQUIRED]
        "species": attackingPokemon["Name"],

        # ability [REQUIRED] (Mold Breaker negates abilities)
        "ability": "Mold Breaker",

        # item [REQUIRED] (Cleanse Tag is practically useless in battle. Items
        # won't give an advantage to either side)
        "item": "Cleanse Tag",

        "level": 100,  # level [REQUIRED], must be a number

        "nature": "Serious",  # not required, defaults to serious

        # not required, defaults to 0 in all stats. Valid stats are "hp", "atk",
        # "spa", "def", "spd", "spe"
        "evs": {},

        "ivs": {}  # not required, defaults to 31 in any stat not specified
    }

    defenderPokemonStats = {
        # species name AS IT IS IN THE POKEDEX  [REQUIRED]
        "species": defendingPokemon["Name"],

        # ability [REQUIRED] (Mold Breaker negates abilities)
        "ability": "Mold Breaker",

        # item [REQUIRED] (Cleanse Tag is practically useless in battle. Items
        # won't give an advantage to either side)
        "item": "Cleanse Tag",

        "level": 100,  # level [REQUIRED], must be a number

        "nature": "Serious",  # not required, defaults to serious

        # not required, defaults to 0 in all stats. Valid stats are "hp", "atk",
        # "spa", "def", "spd", "spe"
        "evs": {},

        "ivs": {}  # not required, defaults to 31 in any stat not specified
    }

    battleObject = {
        "attacker": attackerPokemonStats,
        "defender": defenderPokemonStats,
        "move": moveUsed
    }

    # The response comes in two parts. The first is data, which will be in an
    # object like this:
    response = requests.post(url, json=battleObject)

    # Print the content of the response (the data the server returned)
    battleData = response.json()

    # gets min damage from battle data; uses 0 if not there (defending Pokemon
    # immune to move)
    minDamage = battleData.get("min", 0)

    # gets max damage from battle data; uses 0 if not there (defending Pokemon
    # immune to move)
    maxDamage = battleData.get("max", 0)

    percentageRoll = int(random.uniform(minDamage, maxDamage))
    return percentageRoll


def displayImage(gw):
    """
        Description: Displays the pokemon logo image on the main window
        Parameters: gw, Graphics Window (GraphWin object) to display image
        Return Val: None
        """
    width = gw.getWidth()
    height = gw.getHeight()

    for item in gw.items[:]:
        item.undraw()
    gw.update()

    pokeImg = Image(Point(width / 2, height / 2), "pokelogo.gif")
    pokeImg.draw(gw)


def popupTutorial():
    """
        Description: Displays the Help Button's instruction manual
        Parameters: None
        Return Val: None
    """
    width = 800
    height = 600
    gw = GraphWin("Tutorial", width, height)

    tutorialMessage = """
    Introduction to Competitive Pokémon!
        Welcome to the Instruction Manual.

        Strategy revolves around predicting what your opponent will do and acting accordingly.

        In nearly every game type in Pokémon, the goal is to make your opponent's Pokémon faint, and this is generally done by using moves to deal damage.

        Physical and Special moves:
        All attacking moves are either Physical or Special moves.
        Physical moves use your attacker's Attack stat against your target's Defense stat.
        Special moves use your attacker's Special Attack stat against the target's Special Defense stat.

        Official  Format:
        Our battle simulator is a randomized 1-1 Pokemon battle.
        The list of Pokemon from which your Pokemon is selected are all from competitively viable formats.

        Well, now you have a basic idea of how competitive battling works.
        To start the game, press Exit!
    """
    text = Text(Point(375, 250), tutorialMessage)
    text.draw(gw)

    button = tk.Button(gw, text="Exit", command=gw.close)
    button.place(x=375, y=height - 75)


def findFrames(animation):
    """
        Description: Gets the specific frames needed for the animation
        Parameters: animation (string) of the specific type (ie. grass, fire)
        Return Val: Frames (list of filenames) corresponding to the animation
    """
    folder = "frames"
    frames = []
    for i in range(1, 100):
        filename = os.path.join(folder, animation + "frame" + str(i) + ".gif")
        if not os.path.exists(filename):
            break
        frames.append(filename)
    return frames


def animateMove(window, moveUsed, move2Animation):
    """
        Description: To display the gif images while moving it to the right
        Parameters: window- Graphics Window (GraphWin object),
                    moveUsed- move the user chose (str)
                    move2Animation- move to animation database (dict)

        Return Value: None
    """
    methodName = move2Animation.get(moveUsed)
    if methodName is None:
        print("Error! Cannot find move! ", moveUsed)
        return

    frames = findFrames(methodName.lower())
    if len(frames) == 0:
        frames = findFrames("normal")

    width = window.getWidth()
    height = window.getHeight()

    step = (width / 2 + 100 / 2) / (len(frames) - 1)
    for i in range(len(frames)):
        animationFile = frames[i]
        anchorPt = Point(width / 2 + step * (i - 1), height / 2)
        image = Image(anchorPt, animationFile)
        image.draw(window)
        sleep(0.5)  # adjust as needed for smooth transitions
        image.undraw()
    return


def drawPlayFrame(gw, playersPokemonName, computersPokemonName):
    """
       Description: Creates the frame for the play window (lines, images, etc.)
       Parameters: gw- Graphic Window (object),
                   playersPokemonName- the player's Pokemon's name (str),
                   computersPokemonName- the computer's Pokemon's name (str)
       Return Val: the player's Pokemon's HP Bar (Rectangle Object), the
                   computer's Pokemon's HP Bar (Rectangle Object)
    """
    width = gw.getWidth()
    height = gw.getHeight()

    splitHeight = height * 5 / 6
    line1 = Line(Point(0, splitHeight), Point(width, splitHeight))
    line1.draw(gw)

    line2 = Line(Point(width * 0.2, 0), Point(width * 0.2, splitHeight))
    line2.draw(gw)

    line3 = Line(Point(width * 0.8, 0), Point(width * 0.8, splitHeight))
    line3.draw(gw)

    text1 = Text(Point(width * .1, height * .3), "PLAYER 1 (YOU)")
    text1.draw(gw)
    text2 = Text(Point(width * .9, height * .3), "PLAYER 2 (COMPUTER)")
    text2.draw(gw)

    text1 = Text(Point(width * .1, height * .3 + 50), playersPokemonName)
    text1.draw(gw)
    text2 = Text(Point(width * .9, height * .3 + 50), computersPokemonName)
    text2.draw(gw)

    resizeAndDisplayImage(playersPokemonName, gw, 110, 100, width * 0.1)
    resizeAndDisplayImage(computersPokemonName, gw, 110, 100, width * 0.9)

    playersHPBar = Rectangle(Point(width * .01, height * .16),
                             Point(width * .19, height * .19))
    playersHPBar.setFill("light green")
    playersHPBar.setOutline("light green")
    playersHPBar.draw(gw)

    computersHPBar = Rectangle(Point(width * .81, height * .16),
                               Point(width * .99, height * .19))
    computersHPBar.setFill("light green")
    computersHPBar.setOutline("light green")
    computersHPBar.draw(gw)

    return playersHPBar, computersHPBar


def getMoves(pokemonMovePool):
    """
    Description: Gets a set of four moves from a Pokemon's movepool
    Parameters: the Pokemon's movepool (list of str)
    Return Val: a set of four moves (list of str)
    """
    moveSet = []
    while len(moveSet) < 4:
        move = random.choice(pokemonMovePool)
        if move not in moveSet:
            # ensures that there are no duplicate moves in the set
            moveSet.append(move)

    return moveSet


def disableButtons(move1Button, move2Button, move3Button, move4Button):
    """
    Description: disables four buttons given in parameter
    Parameters: the four buttons (Button object)
    Return Val: None
    """
    move1Button["state"] = "disabled"
    move2Button["state"] = "disabled"
    move3Button["state"] = "disabled"
    move4Button["state"] = "disabled"


def displayDamageText(gw, attackingPokemon, defendingPokemon, moveUsed,
                      damageRoll):
    """
    Description: Displays text related to the move used and a message correlated
                 to the amount of damage it does
    Parameters: gw- the Graphics Window (GraphWin object),
                attackingPokemon- the attacking Pokemon's stats (dict),
                defendingPokemon- the defending Pokemon's stats (dict),
                moveUsed- the move used by the attacking Pokemon (str),
                damageRoll- the amount of damage that move did (int)
    Return Val: None
    """
    width = gw.getWidth()
    height = gw.getHeight()

    moveText = Text(Point(width * .5, height * .8), "%s used %s!" %
                    (attackingPokemon["Name"], moveUsed))
    moveText.draw(gw)
    sleep(2)
    moveText.undraw()

    if damageRoll == 0:
        damageText = Text(Point(width * .5, height * .8), "Yikes! %s is immune "
                                                          "to %s's attack!" %
                          (defendingPokemon["Name"], attackingPokemon["Name"]))
    elif damageRoll < 10:
        damageText = Text(Point(width * .5, height * .8), "Oof, it's not very "
                                                          "effective...")
    elif damageRoll < 40:
        damageText = Text(Point(width * .5, height * .8), "Not bad...!")
    else:
        damageText = Text(Point(width * .5, height * .8), "Ouch!!! That's a LOT"
                                                          " of damage!")
    damageText.draw(gw)
    sleep(2)
    damageText.undraw()


def animateHPDrop(gw, HPBar, damageDone, HPLeft):
    """
    Description: displays the animation for the HP Bar dropping
    Parameters: gw- the Graphics Window (GraphWin object),
                HPBar- the HP bar of a Pokemon (Rectangle object),
                damageDone- the amount of damage done (int),
                HPLeft- the HP the Pokemon has left (int)
    Return Val: None
    """
    if damageDone == 0:
        # no damage done
        return

    HPBar.undraw()
    HPBar.setFill("gray")
    HPBar.setOutline("gray")
    HPBar.draw(gw)

    for i in range(damageDone + 1):
        HPBarP1XCoord = HPBar.getP1().getX()
        HPBarP2XCoord = HPBar.getP2().getX()
        HPBarP2YCoord = HPBar.getP2().getY()
        HPLeftXCoord = HPBarP1XCoord + HPLeft * (
                HPBarP2XCoord - HPBarP1XCoord) / 100
        hpLeftBox = Rectangle(HPBar.getP1(), Point(HPLeftXCoord, HPBarP2YCoord))
        hpLeftBox.setFill("light green")
        hpLeftBox.setOutline("light green")
        hpLeftBox.draw(gw)
        sleep(1.0 / damageDone)
        if i != damageDone:
            # undraws all animation frames except the last
            hpLeftBox.undraw()
        HPLeft -= 1
        if HPLeft == 0:
            # Pokemon has fainted
            break


def doTurn(winPlay, gwMain, computersHPBar, playersHPBar, playersPokemon,
           computersPokemon, playersMove, move1Button, move2Button, move3Button,
           move4Button, HPValues, computersMoves, move2Animation):
    """
    Description: plays one turn in the game
    Parameters: winPlay- the battle Graphics Window (GraphWin object),
                gwMain- the main Graphics Window (GraphWin object),
                computersHPBar- HP bar of computer's Pokemon(Rectangle object),
                playersHPBar- HP bar of player's Pokemon (Rectangle object),
                playersPokemon- the stats of the player's Pokemon (dict),
                computersPokemon- the stats of the computer's Pokemon (dict),
                playersMove- the move the player picked (str),
                move(1,2,3,4)Button- buttons representing each move (Button
                object),
                HPValues - HP Values for Player and Computer (list of ints),
                computersMoves-the computer's Pokemon's moves (list of str)
                move2Animation- move to animation database (dict)
    Return Val: None
    """
    # user's turn has ended, disabling buttons so to prevent from clicking again
    disableButtons(move1Button, move2Button, move3Button, move4Button)
    # animateMove(winPlay, playersMove, move2Animation)
    dropPokemonHP(winPlay, computersHPBar, playersPokemon, computersPokemon,
                  playersMove, HPValues, 1)  # drop computers' HP

    if HPValues[1] <= 0:
        # game over, player won
        endGame(winPlay, gwMain, "You")
        return

    computerMove = random.choice(computersMoves)
    disableButtons(move1Button, move2Button, move3Button, move4Button)
    # animateMove(winPlay, computerMove, move2Animation)
    doComputerMove(winPlay, computerMove, computersPokemon, playersPokemon,
                   move1Button, move2Button, move3Button, move4Button,
                   playersHPBar, HPValues)

    if HPValues[0] <= 0:
        # computer has won, disables buttons
        disableButtons(move1Button, move2Button, move3Button, move4Button)
        endGame(winPlay, gwMain, "Comp")
        return


def doComputerMove(winPlay, computerMove, computersPokemon, playersPokemon,
                   move1Button, move2Button, move3Button, move4Button,
                   playersHPBar, HPValues):
    """
      Description: Does one of the computer's turns
      Parameters: winPlay- the battle Graphics Window (GraphWin object),
                  computerMove- the computer's Pokemon's move (str),
                  computersPokemon- the stats of the computer's Pokemon (dict),
                  playersPokemon- the stats of the player's Pokemon (dict),
                  move(1,2,3,4)Button- buttons representing each move (Button
                  object),
                  HPValues - HP Values for Player and Computer (list of ints),
      Return Val: None
      """
    # user's turn has ended, disabling buttons so to prevent from clicking again
    dropPokemonHP(winPlay, playersHPBar, computersPokemon, playersPokemon,
                  computerMove, HPValues, 0)  # drop player's HP
    # end of computer's turn, reactivating so user can make their move
    reactivateButtons(move1Button, move2Button, move3Button, move4Button)


def reactivateButtons(move1Button, move2Button, move3Button, move4Button):
    """
    Description: Reactivates all four buttons
    Parameters: each of the four buttons (Button object)
    Return Val: None
    """
    move1Button["state"] = "normal"
    move2Button["state"] = "normal"
    move3Button["state"] = "normal"
    move4Button["state"] = "normal"


def dropPokemonHP(gw, defendingHPBar, attackingPokemon, defendingPokemon,
                  moveUsed, HPValues, playerIndex):
    """
    Description: Drops the HP of a given Pokemon
    Parameters: gw- Graphics Window (GraphWin object),
                defendingHPBar- HP bar of defending Pokemon (Rectangle object),
                attackingPokemon- the stats of the attacking Pokemon (dict),
                defendingPokemon- the stats of the defending Pokemon (dict),
                moveUsed- the move used (str),
                HPValues- the amount of HP the defending Pokemon has left (int)
                playerIndex- player index, 0 for player, 1 for computer (int)
    Return Val: None
    """
    damageRoll = calculateDamage(attackingPokemon, defendingPokemon, moveUsed)
    displayDamageText(gw, attackingPokemon, defendingPokemon, moveUsed,
                      damageRoll)
    animateHPDrop(gw, defendingHPBar, damageRoll, HPValues[playerIndex])
    HPValues[playerIndex] -= damageRoll


def playGame(gwMain, pokemonData, move2Animation):
    """
    Description: Plays the Pokemon Game
    Parameters: gwMain- the main Graphics Window (GraphWin object),
                pokemonData- the Pokemon data (list of Pokemon stats)
                move2Animation- move to animation database (dict)
    Return Val: None
    """
    playersPokemon = random.choice(pokemonData)
    playersMoves = getMoves(playersPokemon["Moves"])

    computersPokemon = random.choice(pokemonData)
    computersMoves = getMoves(computersPokemon["Moves"])

    width = 800
    height = 600
    winPlay = GraphWin("Pokemon Battle! ", width, height)
    playersHPBar, computersHPBar = drawPlayFrame(winPlay,
                                                 playersPokemon["Name"],
                                                 computersPokemon["Name"])
    buttonY = height * 0.9
    buttonWidth = 20

    # uses an array so that the lambda function can update the HP values
    HPValues = [100, 100]  # [playersHP, computersHP]

    move1Button = tk.Button(winPlay, width=buttonWidth, text=playersMoves[0],
                            command=lambda: doTurn(winPlay, gwMain,
                                                   computersHPBar,
                                                   playersHPBar, playersPokemon,
                                                   computersPokemon,
                                                   playersMoves[0],
                                                   move1Button, move2Button,
                                                   move3Button, move4Button,
                                                   HPValues,
                                                   computersMoves,
                                                   move2Animation))
    move1Button.place(x=width / 5 - buttonWidth * 5, y=buttonY)

    move2Button = tk.Button(winPlay, width=buttonWidth, text=playersMoves[1],
                            command=lambda: doTurn(winPlay, gwMain,
                                                   computersHPBar,
                                                   playersHPBar, playersPokemon,
                                                   computersPokemon,
                                                   playersMoves[1],
                                                   move1Button, move2Button,
                                                   move3Button, move4Button,
                                                   HPValues,
                                                   computersMoves,
                                                   move2Animation))
    move2Button.place(x=width / 5 * 2 - buttonWidth * 5, y=buttonY)

    move3Button = tk.Button(winPlay, width=buttonWidth, text=playersMoves[2],
                            command=lambda: doTurn(winPlay, gwMain,
                                                   computersHPBar,
                                                   playersHPBar, playersPokemon,
                                                   computersPokemon,
                                                   playersMoves[2],
                                                   move1Button, move2Button,
                                                   move3Button, move4Button,
                                                   HPValues,
                                                   computersMoves,
                                                   move2Animation))
    move3Button.place(x=width / 5 * 3 - buttonWidth * 5, y=buttonY)

    move4Button = tk.Button(winPlay, width=buttonWidth, text=playersMoves[3],
                            command=lambda: doTurn(winPlay, gwMain,
                                                   computersHPBar,
                                                   playersHPBar, playersPokemon,
                                                   computersPokemon,
                                                   playersMoves[3],
                                                   move1Button, move2Button,
                                                   move3Button, move4Button,
                                                   HPValues,
                                                   computersMoves,
                                                   move2Animation))
    move4Button.place(x=width / 5 * 4 - buttonWidth * 5, y=buttonY)

    if computersPokemon["Speed"] > playersPokemon["Speed"]:
        # computer's pokemon is faster, so computer plays first
        disableButtons(move1Button, move2Button, move3Button, move4Button)
        computerMove = random.choice(computersMoves)
        # animateMove(winPlay, computerMove, move2Animation)
        doComputerMove(winPlay, computerMove, computersPokemon,
                       playersPokemon, move1Button, move2Button,
                       move3Button, move4Button, playersHPBar, HPValues)
        if HPValues[0] <= 0:
            endGame(winPlay, gwMain, "Comp")


def endGame(winPlay, gwMain, winner):
    """
    Description: Displays endgame messages
      Parameters: winPlay- the battle Graphics Window (GraphWin object),
                  gwMain- the main Graphics Window (GraphWin object),
                  winner- the winner (str)
      Return Val: None
    """
    if winner == "You":
        endMessage = "You win! Congrats!"
    else:
        endMessage = "You lose."

    endMessage += "\nAre you sure you want to exit the application"
    userChoice = tk.messagebox.askquestion("Exit Application",
                                           endMessage, icon='warning')
    if userChoice == 'yes':
        # user wants to quit
        winPlay.close()
        gwMain.quit()
    else:
        winPlay.close()


def main():
    pokemonData = readPokeFile("pokemon-data.csv")
    move2Animation = readMoveFile()

    width = 800
    height = 500
    gwMain = GraphWin("Pokemon Battles! ", width, height)

    displayImage(gwMain)

    buttonY = height * 0.9
    buttonWidth = 20

    helpButton = tk.Button(gwMain, width=buttonWidth, text="Help",
                           command=popupTutorial)
    helpButton.place(x=width / 4 - buttonWidth * 5, y=buttonY)

    playButton = tk.Button(gwMain, width=buttonWidth, text="Play",
                           command=lambda: playGame(gwMain, pokemonData,
                                                    move2Animation))
    playButton.place(x=width / 4 * 2 - buttonWidth * 5, y=buttonY)

    quitButton = tk.Button(gwMain, width=buttonWidth, text="Quit",
                           command=gwMain.quit)
    quitButton.place(x=width / 4 * 3 - buttonWidth * 5, y=buttonY)

    gwMain.mainloop()


main()
