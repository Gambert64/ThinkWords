# Think Words Game

Think Words is an interactive word game built with Python and Tkinter. The game challenges players to think of words within a given category while racing against the clock.

## Features

- Multiplayer support (2-8 players)
- Customizable game settings:
  - Adjustable timer duration
  - Customizable points required to win
- Timer-based gameplay
- Category-based word challenges
- Score tracking
- German language support
- Responsive GUI that adapts to screen size

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)
- Pillow (PIL) for image handling

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Launch the game by running:
   ```bash
   python game.py
   ```
2. Configure game settings:
   - Set your preferred timer duration
   - Set the number of points required to win
   - Choose language (German/English)
3. Enter player names in the lobby (2-8 players)
4. Start the game
5. When it's your turn:
   - A category will be displayed
   - Click on a letter to start the timer
   - Think of a word that fits the category and starts with the selected letter
   - If you fail or time runs out, it's the next player's turn
6. The first player to reach the target score wins!

## Game Rules

- Each player takes turns
- You have a customizable amount of time to think of a word
- Words must:
  - Start with the selected letter
  - Fit the given category

## Project Structure

- `game.py` - Main game logic and GUI
- `icons/` - Directory containing game icons
- `requirements.txt` - Project dependencies

## Contributing

Feel free to fork this project and submit pull requests with improvements or new features.
