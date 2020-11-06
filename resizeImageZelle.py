"""
    Description: This program demonstrates how to load, resize, and display an
                 image file (that's stored locally on your computer).
    Author: Mr. Bloom
    Date: Spring 2020
"""

import graphics
from PIL import Image, ImageTk
import requests
from io import BytesIO

#------------------------------------------------------------------------------#
def resizeAndDisplayImage(pokemon, window, imgWidth, imgHeight, coordx):

    # Path and filename for image file (can be .GIF .JPG or .PNG format)
    filename = "%s.png" % pokemon

    # Open the image file and resize to specified dimensions
    imageTmp = Image.open("sprites/" + filename)
    newDimesions = (imgWidth, imgHeight)
    imageTmp = imageTmp.resize(newDimesions, Image.ANTIALIAS)

    # Save the resized image as a separate file (by changing filename)
    filename = "NEW_" + filename
    imageTmp.save("sprites/"+ filename)

    # Load the resized image and convert to (Tkinter Graphics) Image object
    photo = ImageTk.PhotoImage(file="sprites/" + filename)

    # Display image file (must be in .GIF format)
    anchorPt = graphics.Point(coordx, window.getHeight()/2)
    pokedexImg = graphics.Image(anchorPt, "sprites/" + filename)
    pokedexImg.draw(window)

    return
#------------------------------------------------------------------------------#
def main():
    gw = graphics.GraphWin("Resize and Display Image Example", 600, 600)

    gw.getMouse()
    gw.close()

if __name__ == "__main__":
    main()
