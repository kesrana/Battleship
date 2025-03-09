# **Battleship Game - Pygame Project**

![image](https://github.com/user-attachments/assets/0ccb510e-fe6e-4cbf-b3d0-c860bb097469)



Overview

This is a Python-based implementation of the classic Battleship game using the Pygame library. The game features a graphical user interface (GUI) where players can place ships, attempt to guess their opponent’s ship locations, and track the game state with features such as sound, difficulty selection, and a mute option. The game also includes functionality to adjust volume and switch between difficulty levels.

Features

	•	Gameplay: Players can place ships on their grid, and take turns guessing the opponent’s ship locations.
	•	Volume Control: Players can mute the sound and adjust the volume of background music.
	•	Difficulty Levels: The game allows toggling between different difficulty settings.
	•	Ship Placement: Ships are placed on the player’s board, and the opponent’s ships are randomly generated.
	•	Sound: Background music plays during the game with sound effects for hits and misses.
	•	Graphics: The game features a user-friendly graphical interface with buttons and a game board.

Requirements

	•	Python 3.x
	•	Pygame library

You can install the Pygame library by running:

```pip install pygame```

Installation

	1.	Clone the repository or download the source files.
	2.	Ensure Python 3 and Pygame are installed.
	3.	Run the game by executing the main.py file:

```python game.py```

How to Play

	1.	Start the Game: Once the game loads, you’ll be prompted to place your ships.
	2.	Place Ships: Click on the grid to place your ships (each ship will take up a certain number of spaces). Once you’re done, confirm your ship placement.
	3.	Guess Opponent’s Ships: After ship placement, the game will allow you to start guessing the opponent’s ship locations.
	4.	Use Buttons: Use the buttons for additional options, such as muting the sound, changing the difficulty, or going back to the main menu.

Controls

	•	Left-click on the game grid to select cells and place ships or make guesses.
	•	Escape Key (ESC): Access the settings menu for options like volume control and difficulty selection.
	•	Mute Button: Toggle the game sound on or off.

File Structure

	•	game.py: Main game logic, including event handling, rendering, and state updates.
	•	button.py: Contains the Button class to create interactive buttons in the GUI.
	•	constant.py: Stores constants for colours, screen dimensions, and other game settings.
	•	assets/: Contains images and other resources used in the game (e.g., button images, background music, etc.).
