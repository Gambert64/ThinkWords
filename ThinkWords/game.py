import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import time
import math
from typing import List, Dict
import os
from PIL import Image, ImageTk

class ThinkWordsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Think Words!")
        
        # Initialize window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Center the window on the screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"+{x}+{y}")
        
        self.load_icons()
        
        # Initialize game settings and state
        self.timer_duration = 30  # Default timer duration in seconds
        self.points_to_win = 10   # Default points needed to win
        self.language = "deutsch" # Default language
        
        # Game state variables
        self.current_category = ""  # Current category for word guessing
        self.players: List[str] = []  # List of player names
        self.current_player_index = 0  # Index of current player
        self.scores: Dict[str, int] = {}  # Dictionary to track player scores
        self.game_active = False  # Flag to indicate if game is in progress
        self.timer_running = False  # Flag to indicate if timer is active
        self.time_left = self.timer_duration  # Remaining time in current round
        self.used_letters = set()  # Set of letters already used in current round
        self.timer_id = None  # ID of the current timer
        
        self.create_widgets()
        
    def load_icons(self):
        if not os.path.exists("icons"):
            os.makedirs("icons")
        try:
            self.root.iconphoto(True, tk.PhotoImage(file="icons/logo.png"))
        except:
            pass
            
    def create_widgets(self):
        self.settings_frame = tk.Frame(self.root)
        self.settings_frame.pack(pady=10)
        
        tk.Label(self.settings_frame, text="Timer (Sekunden):").pack(side=tk.LEFT, padx=5)
        self.timer_spinbox = ttk.Spinbox(self.settings_frame, from_=1, to=float('inf'), width=5)
        self.timer_spinbox.set(self.timer_duration)
        self.timer_spinbox.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.settings_frame, text="Punkte zum Sieg:").pack(side=tk.LEFT, padx=5)
        self.points_spinbox = ttk.Spinbox(self.settings_frame, from_=1, to=float('inf'), width=5)
        self.points_spinbox.set(self.points_to_win)
        self.points_spinbox.pack(side=tk.LEFT, padx=5)
        
        self.language_frame = tk.Frame(self.settings_frame)
        self.language_frame.pack(side=tk.LEFT, padx=10)
        
        self.language_var = tk.StringVar(value=self.language)
        ttk.Radiobutton(self.language_frame, text="Deutsch", variable=self.language_var, 
                      value="deutsch", command=lambda: self.set_language("deutsch")).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(self.language_frame, text="English", variable=self.language_var, 
                      value="english", command=lambda: self.set_language("english")).pack(side=tk.LEFT, padx=5)
        
        self.player_header_frame = tk.Frame(self.root)
        self.player_header_frame.pack(pady=10)
        
        self.player_labels = {}
        
        self.category_label = tk.Label(
            self.root, 
            text="Gebe die Namen der Spieler ein (2-8)",
            font=("Arial", 24)
        )
        self.category_label.pack(pady=30)
        
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=10)
        
        self.player_entries = []
        for i in range(8):
            entry = tk.Entry(self.player_frame, width=20)
            entry.pack(pady=5)
            self.player_entries.append(entry)
            
        self.start_button = tk.Button(
            self.root,
            text="Spiel starten",
            command=self.start_game,
            font=("Arial", 16),
            width=20,
            height=3
        )
        self.start_button.pack(pady=20)
        
        self.timer_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 24)
        )
        
        self.return_button = tk.Button(
            self.root,
            text="Zurück zur Lobby",
            command=self.return_to_lobby,
            font=("Arial", 12)
        )
        
    def set_language(self, lang):
        self.language = lang
        self.update_texts()
        
    def update_texts(self):
        if self.language == "deutsch":
            texts = {
                "timer": "Timer (Sekunden):",
                "points": "Punkte zum Sieg:",
                "category": "Kategorie:",
                "time_left": "Zeit: {}s",
                "time_up": "Zeit abgelaufen",
                "player_out": "{} ist raus!",
                "game_over": "Spiel beendet",
                "winner": "{} hat gewonnen!",
                "enter_names": "Gebe die Namen der Spieler ein (2-8)",
                "start_game": "Spiel starten",
                "return_lobby": "Zurück zur Lobby",
                "enter_category": "Kategorie eingeben",
                "category_prompt": "{}, gib eine Kategorie ein:",
                "point_for": "Punkt für {}",
                "round_over": "Runde beendet",
                "all_players_back": "{} hat einen Punkt bekommen! Alle Spieler kommen zurück!"
            }
        else:
            texts = {
                "timer": "Timer (Seconds):",
                "points": "Points to Win:",
                "category": "Category:",
                "time_left": "Time: {}s",
                "time_up": "Time's up",
                "player_out": "{} is out!",
                "game_over": "Game Over",
                "winner": "{} has won!",
                "enter_names": "Enter player names (2-8)",
                "start_game": "Start Game",
                "return_lobby": "Return to Lobby",
                "enter_category": "Enter Category",
                "category_prompt": "{}, enter a category:",
                "point_for": "Point for {}",
                "round_over": "Round Over",
                "all_players_back": "{} got a point! All players are back!"
            }
            
        self.timer_spinbox.master.children["!label"].config(text=texts["timer"])
        self.points_spinbox.master.children["!label"].config(text=texts["points"])
        self.category_label.config(text=texts["enter_names"])
        self.start_button.config(text=texts["start_game"])
        self.return_button.config(text=texts["return_lobby"])
        
    def return_to_lobby(self):
        # Reset game state
        self.game_active = False
        self.current_category = ""
        self.used_letters = set()
        self.players = []
        self.scores = {}
        
        # Clear all widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Recreate all widgets
        self.create_widgets()
        
        # Update settings
        self.timer_duration = int(self.timer_spinbox.get())
        self.points_to_win = int(self.points_spinbox.get())
        
    def start_game(self):
        # Get player names
        self.players = [entry.get() for entry in self.player_entries if entry.get().strip()]
        
        if len(self.players) < 2 or len(self.players) > 8:
            messagebox.showerror("Error" if self.language == "english" else "Fehler", 
                               "Please enter 2-8 players" if self.language == "english" else "Bitte 2-8 Spieler eingeben!")
            return
            
        # Get settings from spinboxes
        self.timer_duration = int(self.timer_spinbox.get())
        self.points_to_win = int(self.points_spinbox.get())
            
        # Initialize scores
        self.scores = {player: 0 for player in self.players}
        self.current_player_index = 0
        self.used_letters = set()
        self.time_left = self.timer_duration
        
        # Clear all widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create game board
        self.create_game_board()
        
        # Show return button
        self.return_button.pack(pady=10)
        
        # Start first round
        self.start_round()
        
    def create_game_board(self):
        # Create player header
        self.player_header_frame = tk.Frame(self.root)
        self.player_header_frame.pack(pady=10)
        self.update_player_header()
        
        # Create letter buttons in keyboard layout
        self.letter_buttons = {}
        
        # QWERTY keyboard layout
        keyboard_rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        
        # Get window dimensions
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Calculate starting positions based on window size
        start_x = window_width // 2 - 200  # Center horizontally
        start_y = window_height // 2 - 100  # Center vertically
        button_width = 40
        button_height = 40
        row_spacing = 50
        col_spacing = 45
        
        for row_idx, row in enumerate(keyboard_rows):
            # Calculate y position for this row
            y = start_y + (row_idx * row_spacing)
            
            # Calculate x offset for each row to create the staggered keyboard effect
            x_offset = 0
            if row_idx == 1:  # Second row
                x_offset = button_width // 2
            elif row_idx == 2:  # Third row
                x_offset = button_width
            
            for col_idx, letter in enumerate(row):
                x = start_x + (col_idx * col_spacing) + x_offset
                
                btn = tk.Button(
                    self.root,
                    text=letter,
                    command=lambda l=letter: self.letter_clicked(l),
                    width=3,
                    height=1
                )
                btn.place(x=x, y=y)
                self.letter_buttons[letter] = btn
        
        # Create score buttons
        self.score_buttons_frame = tk.Frame(self.root)
        self.score_buttons_frame.pack(pady=10)
        
        for player in self.players:
            btn = tk.Button(
                self.score_buttons_frame,
                text=self.get_text("point_for").format(player),
                command=lambda p=player: self.add_score(p),
                width=15
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Create timer label
        self.timer_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 24)
        )
        self.timer_label.pack(pady=10)
        
        # Create category label
        self.category_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 24)
        )
        self.category_label.place(x=window_width//2 - 100, y=start_y - 100)
        
        # Create return button at the bottom
        self.return_button = tk.Button(
            self.root,
            text=self.get_text("return_lobby"),
            command=self.return_to_lobby,
            font=("Arial", 12)
        )
        self.return_button.pack(side=tk.BOTTOM, pady=20)
        
    def get_text(self, key):
        texts = {
            "deutsch": {
                "timer": "Timer (Sekunden):",
                "points": "Punkte zum Sieg:",
                "category": "Kategorie:",
                "time_left": "Zeit: {}s",
                "time_up": "Zeit abgelaufen",
                "player_out": "{} ist raus!",
                "game_over": "Spiel beendet",
                "winner": "{} hat gewonnen!",
                "enter_names": "Gebe die Namen der Spieler ein (2-8)",
                "start_game": "Spiel starten",
                "return_lobby": "Zurück zur Lobby",
                "enter_category": "Kategorie eingeben",
                "category_prompt": "{}, gib eine Kategorie ein:",
                "point_for": "Punkt für {}",
                "round_over": "Runde beendet",
                "all_players_back": "{} hat einen Punkt bekommen! Alle Spieler kommen zurück!"
            },
            "english": {
                "timer": "Timer (Seconds):",
                "points": "Points to Win:",
                "category": "Category:",
                "time_left": "Time: {}s",
                "time_up": "Time's up",
                "player_out": "{} is out!",
                "game_over": "Game Over",
                "winner": "{} has won!",
                "enter_names": "Enter player names (2-8)",
                "start_game": "Start Game",
                "return_lobby": "Return to Lobby",
                "enter_category": "Enter Category",
                "category_prompt": "{}, enter a category:",
                "point_for": "Point for {}",
                "round_over": "Round Over",
                "all_players_back": "{} got a point! All players are back!"
            }
        }
        return texts[self.language][key]
        
    def start_round(self):
        # Only ask for category if it's the first round or after a point was awarded
        if not self.current_category:
            # Ask for category
            self.current_category = simpledialog.askstring(
                self.get_text("enter_category"),
                self.get_text("category_prompt").format(self.players[self.current_player_index])
            )
            
            if not self.current_category:
                self.current_category = "Allgemein" if self.language == "deutsch" else "General"
                
        self.category_label.config(text=f"{self.get_text('category')} {self.current_category}")
        self.category_label.place(x=400, y=200)
        
        self.game_active = True
        self.timer_running = True
        self.time_left = self.timer_duration
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.update_timer()
        self.update_player_header()
        
    def letter_clicked(self, letter):
        if not self.game_active or letter in self.used_letters:
            return
            
        # Block the letter
        self.used_letters.add(letter)
        self.letter_buttons[letter].config(state=tk.DISABLED, bg='gray')
        
        # Reset timer and move to next player
        self.timer_running = True
        self.time_left = self.timer_duration
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.update_timer()
        self.next_player()
        
    def add_score(self, player):
        if not self.game_active:
            return
            
        # Award point to player and update display
        self.scores[player] += 1
        self.update_player_header()
        
        # Check if player has reached the required points to win
        if self.scores[player] == self.points_to_win:
            messagebox.showinfo(
                self.get_text("game_over"),
                self.get_text("winner").format(player)
            )
            self.game_active = False
            self.return_to_lobby()
            return
            
        # Prepare for next player's turn
        self.used_letters = set()  # Reset used letters
        self.reset_letter_buttons()  # Reset letter buttons
        self.current_category = ""  # Clear category for new round
        self.next_player()  # Move to next player
        
    def reset_letter_buttons(self):
        for letter, button in self.letter_buttons.items():
            button.config(state=tk.NORMAL, bg='SystemButtonFace')
            
    def update_timer(self):
        if self.timer_running:
            # Update timer display
            self.timer_label.config(text=self.get_text("time_left").format(self.time_left))
            if self.time_left > 0:
                # Decrease time and schedule next update
                self.time_left -= 1
                self.timer_id = self.root.after(1000, self.update_timer)
            else:
                # Time's up - handle player elimination
                self.timer_running = False
                messagebox.showinfo(
                    self.get_text("time_up"),
                    self.get_text("player_out").format(self.players[self.current_player_index])
                )
                self.players.pop(self.current_player_index)
                
                # Check if only one player remains
                if len(self.players) == 1:
                    # Award point to last remaining player
                    self.scores[self.players[0]] += 1
                    self.update_player_header()
                    
                    # Check if this point wins the game
                    if self.scores[self.players[0]] == self.points_to_win:
                        messagebox.showinfo(
                            self.get_text("game_over"),
                            self.get_text("winner").format(self.players[0])
                        )
                        self.return_to_lobby()
                        return
                    
                    # If game continues, bring back all eliminated players
                    messagebox.showinfo(
                        self.get_text("round_over"),
                        self.get_text("all_players_back").format(self.players[0])
                    )
                    # Restore all players for next round
                    self.players = list(self.scores.keys())
                    self.current_player_index = self.players.index(self.players[0])
                    self.used_letters = set()
                    self.reset_letter_buttons()
                    self.start_round()
                else:
                    # Move to next player if multiple players remain
                    self.next_player()
                
    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.update_player_header()
        self.start_round()

    def update_player_header(self):
        for widget in self.player_header_frame.winfo_children():
            widget.destroy()
            
        for i, player in enumerate(self.players):
            bg_color = "lightgreen" if i == self.current_player_index else "SystemButtonFace"
            label = tk.Label(
                self.player_header_frame,
                text=f"{player}: {self.scores[player]} Punkte",
                font=("Arial", 14),
                bg=bg_color,
                padx=20,
                pady=10
            )
            label.pack(side=tk.LEFT, padx=5)
            self.player_labels[player] = label

if __name__ == "__main__":
    root = tk.Tk()
    game = ThinkWordsGame(root)
    root.mainloop() 