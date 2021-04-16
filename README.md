This project goes with another project of mine : KinetikCreator => https://github.com/Toshibane/KinetikCreator.

It's a Visual Novel Reader, using JSON files as a base, and fully written in Python with Pygame as a sole dependency.

## HOW IT WORKS

First, there's a main menu, allowing to choose what to do : start a new game, load a save file, change configurations, and leave the game.

When starting a new game, or loading a save, you can press Enter or the Spacebar to go to the next dialogue; or press the Escape button to go access a pause menu.

In the pause menu, you can save your current progress, load another save file, enter the configuration menu, or return to the main menu.

Finally, in the configuration menu, you can change the volume of the background music, or toggle fullscreen.

## CODE BASICS

Every menu in the game has its own class, with some basic functions as render make it visible, and start to open the menu.

Then, there are two items created for UI : KineticButton and TextDisplay.

KineticButton is a button, with a render function, and basic functions to change the text, get the value or handle the hover functionality.

TextDisplay is a textbox, allowing to display as much text as we want on screen.

Finally, there is a utils.py file, containing every useful functions such as save/load configuration, or managing save files.
