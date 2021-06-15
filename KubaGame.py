# Author: Ron Riza
# Date: 05/27/2021
# Description: Defines a class KubaGame that represents a game of Kuba and implements its rules
#   through its methods. Rules can be found at https://sites.google.com/site/boardandpieces/list-of-games/kuba.
#   Also defines a class Player that represents the players of the game. Instances are to be used within
#   the KubaGame class through composition.


class KubaGame:
    """A class to represent a KubaGame instance."""

    def __init__(self, player_1, player_2):
        """Initializes the KubaGame instance.

        Parameters
        ----------
        player_1 : tuple
            name (str), color (str) of player 1
        player_2 : tuple
            name (str), color (str) of player 2
        """
        #: tuple of Player instances
        self._players = Player(player_1), Player(player_2)
        #: list of lists:  represents the state of the game board
        self._board = [['W', 'W', 'X', 'X', 'X', 'B', 'B'], ['W', 'W', 'X', 'R', 'X', 'B', 'B'],
                       ['X', 'X', 'R', 'R', 'R', 'X', 'X'], ['X', 'R', 'R', 'R', 'R', 'R', 'X'],
                       ['X', 'X', 'R', 'R', 'R', 'X', 'X'], ['B', 'B', 'X', 'R', 'X', 'W', 'W'],
                       ['B', 'B', 'X', 'X', 'X', 'W', 'W']]
        #: str: the name of the player with the current turn
        self._current_turn = None
        #: str: the name of the player with the current turn
        self._winner = None
        #: list of lists: represents the previous state of the game board before last move was made
        self._previous_state = None

    def display(self):
        """Prints the current state of the board."""
        print('-------------------------')
        for row in self._board:
            print(" | ".join(row))
            print('-------------------------')
        print('\n')

    def make_move(self, player_name, coordinates, direction):
        """Attempts to move marble at coordinates in the direction specified.

        Parameters
        ----------
        player_name : str
            name of player making the move
        coordinates : tuple
            tuple of integers represents row,column
        direction : str
            direction to move marble (possible directions are 'L', 'R', 'F', 'B')

        Returns
        -------
        bool
            True if successful, False otherwise
        """
        player = self.get_player(player_name)
        opponent = self.get_opponent(player_name)
        row = coordinates[0]
        column = coordinates[1]
        if player is None:  # checks if player exists
            return False
        if self.get_winner():   # checks if game has been won
            return False
        if self._current_turn == opponent.get_name():   # checks if current turn belongs to opponent
            return False
        if row < 0 or row > 6 or column < 0 or column > 6:  # checks if coordinates are valid
            return False
        if self.get_marble(coordinates) != player.get_color():  # checks if marble being pushed matches player's color
            return False
        move_successful = self.check_move(player, opponent, row, column, direction, True)
        if move_successful is False:    # checks if move was successful
            return False
        self.check_win(player, opponent)    # checks if move results in a win condition
        return True

    def check_move(self, player, opponent, row, column, direction, process_move):
        """Checks if move is legal, and processes it if specified.

        Parameters
        ----------
        player : Player
            Player instance attempting the move
        opponent : Player
            Player instance of the opponent of the player making the move
        row : int
            row of marble being moved
        column : int
            column of marble being moved
        direction : str
            direction to move marble (possible directions are 'L', 'R', 'F', 'B')
        process_move : bool
            if True, move is processed

        Returns
        -------
        bool
            True if move is valid, False otherwise
        """
        copy_board = [list(row) for row in self._board]     # makes a deep copy of the board for testing
        captured_red = False    # used to determine if a red marble is captured
        knocked_off_opponent = False    # used to determine if opponent marble is knocked off

        if direction == 'L':
            if column == 6 or copy_board[row][column+1] == 'X':     # checks if space is available for pushing
                if 'X' not in copy_board[row][0:column]:    # checks if push will knock a marble off
                    if copy_board[row][0] == player.get_color():  # checks if marble to be knocked off is player's
                        return False
                    elif copy_board[row][0] == 'R':     # checks if marble to be knocked off is red
                        captured_red = True
                    elif copy_board[row][0] == opponent.get_color():
                        knocked_off_opponent = True     # checks if marble to be knocked off belongs to opponent
                    copy_board[row][0] = 'X'            # replace knocked off marble with empty space
                # moves all consecutive marbles until an empty space is reached
                prev = None
                while prev != 'X':
                    if prev is None:
                        prev = 'X'
                    current = copy_board[row][column]
                    copy_board[row][column] = prev
                    prev = current
                    column -= 1
            else:
                return False

        elif direction == 'R':
            if column == 0 or copy_board[row][column-1] == 'X':     # checks if space is available for pushing
                if 'X' not in copy_board[row][column:]:     # checks if push will knock a marble off
                    if copy_board[row][6] == player.get_color():  # checks if marble to be knocked off is player's
                        return False
                    elif copy_board[row][6] == 'R':     # checks if marble to be knocked off is red
                        captured_red = True
                    elif copy_board[row][6] == opponent.get_color():
                        knocked_off_opponent = True     # checks if marble to be knocked off belongs to opponent
                    copy_board[row][6] = 'X'    # replace knocked off marble with empty space
                # moves all consecutive marbles until an empty space is reached
                prev = None
                while prev != 'X':
                    if prev is None:
                        prev = 'X'
                    current = copy_board[row][column]
                    copy_board[row][column] = prev
                    prev = current
                    column += 1
            else:
                return False

        elif direction == 'F':
            if row == 6 or copy_board[row+1][column] == 'X':    # checks if space is available for pushing
                if 'X' not in [copy_board[i][column] for i in range(row)]:  # checks if push will knock a marble off
                    if copy_board[0][column] == player.get_color():    # checks if marble to be knocked off is player's
                        return False
                    elif copy_board[0][column] == 'R':      # checks if marble to be knocked off is red
                        captured_red = True
                    elif copy_board[0][column] == opponent.get_color():
                        knocked_off_opponent = True         # checks if marble to be knocked off belongs to opponent
                    copy_board[0][column] = 'X'     # replace knocked off marble with empty space
                # moves all consecutive marbles until an empty space is reached
                prev = None
                while prev != 'X':
                    if prev is None:
                        prev = 'X'
                    current = copy_board[row][column]
                    copy_board[row][column] = prev
                    prev = current
                    row -= 1
            else:
                return False

        elif direction == 'B':
            if row == 0 or copy_board[row-1][column] == 'X':    # checks if space is available for pushing
                if 'X' not in [copy_board[i][column] for i in range(row, 7)]:  # checks if push will knock a marble off
                    if copy_board[6][column] == player.get_color():    # checks if marble to be knocked off is player's
                        return False
                    elif copy_board[6][column] == 'R':      # checks if marble to be knocked off is red
                        captured_red = True
                    elif copy_board[6][column] == opponent.get_color():
                        knocked_off_opponent = True         # checks if marble to be knocked off belongs to opponent
                    copy_board[6][column] = 'X'
                # moves all consecutive marbles until an empty space is reached
                prev = None
                while prev != 'X':
                    if prev is None:
                        prev = 'X'
                    current = copy_board[row][column]
                    copy_board[row][column] = prev
                    prev = current
                    row += 1
            else:
                return False
        else:
            return False

        if copy_board == self._previous_state:      # checks if move will repeat previous game state
            return False
        else:
            if process_move:        # checks if move is meant to be processed
                self._previous_state = self._board      # sets the previous state to the current state
                self._board = copy_board                # sets the current state to the copy state
                if captured_red:
                    player.add_red_marble()       # if a red marble was captured, add to player's red marble count
                    self._current_turn = player.get_name()  # repeat turn if red marble is captured
                elif knocked_off_opponent:
                    self._current_turn = player.get_name()  # repeat turn if opponent marble is knocked off
                else:
                    self._current_turn = opponent.get_name()    # changes turn
            return True

    def check_all_moves(self, player, opponent):
        """Checks if player has any moves available. If no move is available, opponent is declared winner

        Parameters
        ----------
        player : Player
            the player whose moves will be checked
        opponent : Player
            the opponent of the player whose moves will be checked
        """
        # loops through every position on board
        for row in range(7):
            for column in range(7):
                if self.get_marble((row, column)) == player.get_color():  # checks if marble at position is player's
                    for direction in ['L', 'R', 'F', 'B']:      # tests moves in each direction
                        if self.check_move(player, opponent, row, column, direction, False):
                            return
        self._winner = opponent.get_name()

    def check_win(self, player, opponent):
        """Checks if a win condition has been reached after a move is made.
        If a win condition is met, the _winner attribute is updated.

        Parameters
        ----------
        player : Player
            the player who has just made a move
        opponent : Player
            the opponent of the player who has just made a move
        """
        if player.get_red_marbles() == 7:       # checks if player captured 7 red marbles
            self._winner = player.get_name()

        # checks if opponent has any marbles left (depending on player's color)
        elif player.get_color() == 'W' and self.get_marble_count()[1] == 0:
            self._winner = player.get_name()
        elif player.get_color() == 'B' and self.get_marble_count()[0] == 0:
            self._winner = player.get_name()

        # checks if either player or opponent has any moves left (depending on current turn)
        elif player.get_name() == self._current_turn:
            self.check_all_moves(player, opponent)
        elif opponent.get_name() == self._current_turn:
            self.check_all_moves(opponent, player)

    def get_current_turn(self):
        """Returns the name (str) of the player whose turn it is to play. If no player has made a move, returns None."""
        return self._current_turn

    def get_winner(self):
        """Returns the name (str) of the winning player. If no player has won yet, returns None."""
        return self._winner

    def get_captured(self, player_name):
        """Returns the number (int) of red marbles captured by chosen player."""
        chosen_player = self.get_player(player_name)
        if chosen_player:
            return chosen_player.get_red_marbles()

    def get_player(self, player_name):
        """Returns the Player instance corresponding to player_name. If player does not exist, returns None."""
        chosen_player = None
        for player in self._players:
            if player_name == player.get_name():
                chosen_player = player
        return chosen_player

    def get_opponent(self, player_name):
        """Returns the Player instance of the opponent of player_name."""
        opponent = None
        for player in self._players:
            if player_name != player.get_name():
                opponent = player
        return opponent

    def get_marble(self, coordinates):
        """Returns marble (str) at the location of coordinates. If no marble is present returns 'X'."""
        return self._board[coordinates[0]][coordinates[1]]

    def get_marble_count(self):
        """Returns the number of white marbles, black marbles, and red marbles as a tuple of strings, in that order."""
        marble_count = {'W': 0, 'B': 0, 'R': 0, 'X': 0}
        for row in self._board:
            for location in row:
                marble_count[location] += 1
        return marble_count['W'], marble_count['B'], marble_count['R']


class Player:
    """A class to represent a Player instance"""

    def __init__(self, player_info):
        """Initializes the Player instance.

        Parameters
        ----------
        player_info : tuple
            name (str), color (str) of player
        """
        #: str: name of player
        self._name = player_info[0]
        #: str: color of player's marbles
        self._color = player_info[1]
        #: int: number of red marbles player has captured
        self._red_marbles = 0

    def add_red_marble(self):
        """Adds a red marble to the player's count of captured red marbles"""
        self._red_marbles += 1

    def get_name(self):
        """Returns the name of the player (str)"""
        return self._name

    def get_color(self):
        """Returns the player's color (str)"""
        return self._color

    def get_red_marbles(self):
        """Returns the number (int) of red marbles the player has captured"""
        return self._red_marbles

# game = KubaGame(("A", "W"), ("B", "B"))

# tests red marble win
# print(game.make_move("A", (6,5), 'F'))
# print(game.make_move("B", (0,5), 'B'))
# print(game.make_move("A", (5,5), 'F'))
# print(game.make_move("B", (6,1), 'F'))
# print(game.make_move("A", (4,5), 'F'))
# print(game.make_move("A", (3,5), 'L'))
# print(game.make_move("B", (4,1), 'R'))
# print(game.make_move("A", (3,4), 'L'))
# print(game.make_move("A", (3,3), 'L'))
# print(game.make_move("A", (3,2), 'L'))
# print(game.make_move("A", (3,1), 'L'))
# print(game.make_move("A", (2,5), 'L'))
# print(game.make_move("B", (4,2), 'R'))
# print(game.make_move("A", (2,4), 'L'))
# print(game.make_move("B", (4,3), 'R'))
# print(game.make_move("B", (4,4), 'R'))
# print(game.make_move("B", (4,5), 'R'))
# print(game.make_move("B", (4,6), 'B'))
# print(game.make_move("B", (5,6), 'B'))
# print(game.make_move("B", (6,6), 'L'))
# print(game.make_move("A", (2,3), 'L'))
# print(game.make_move("A", (2,2), 'L'))
# print(game.make_move("A", (2,1), 'L'))

# tests no more moves wins
# print(game.make_move("A", (6,6), 'F'))
# print(game.make_move("B", (0,6), 'B'))
# print(game.make_move("A", (5,6), 'F'))
# print(game.make_move("B", (6,0), 'F'))
# print(game.make_move("A", (4,6), 'F'))
# print(game.make_move("B", (4,0), 'B'))
# print(game.make_move("A", (3,6), 'F'))
# print(game.make_move("A", (2,6), 'F'))
# print(game.make_move("A", (6,5), 'F'))
# print(game.make_move("B", (6,0), 'F'))
# print(game.make_move("A", (5,5), 'F'))
# print(game.make_move("B", (4,0), 'B'))
# print(game.make_move("A", (4,5), 'F'))
# print(game.make_move("A", (3,5), 'F'))
# print(game.make_move("A", (0,1), 'B'))
# print(game.make_move("B", (6,1), 'F'))
# print(game.make_move("A", (1,1), 'B'))
# print(game.make_move("B", (6,0), 'F'))
# print(game.make_move("A", (2,1), 'B'))
# print(game.make_move("A", (3,1), 'B'))
# print(game.make_move("A", (5,1), 'L'))
# print(game.make_move("A", (0,0), 'B'))
# print(game.make_move("B", (4,0), 'R'))
# print(game.make_move("A", (1,0), 'B'))
# print(game.make_move("B", (4,1), 'B'))
# print(game.make_move("A", (2,0), 'R'))
# print(game.make_move("B", (5,1), 'B'))
# print(game.make_move("B", (6,1), 'F'))
# print(game.make_move("A", (5,0), 'F'))
# print(game.make_move("B", (5,1), 'F'))
# print(game.make_move("A", (0,6), 'B'))
# print(game.make_move("B", (4,1), 'F'))
# print(game.make_move("A", (4,0), 'R'))
#
# game.display()
