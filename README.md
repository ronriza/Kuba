# Kuba

Command line implementation of 1997 board game Kuba. Rules can be found here: https://sites.google.com/site/boardandpieces/list-of-games/kuba

To initialize:
`game = KubaGame((player_name, color), (player_name, color))   # where color is either "B" or "W"`

To make a move:
`game.make_move(player_name, coordinates, direction)   # where coordinates are a tuple of (row, col) and direction is one of: "L", "R", F", "B"`

To display current baord:
`game.display()`
