# | id | x | y | angle | velX | VelY | health | accelerating | shooting | alive
PLAYER_STATE_FORMAT = "i 8s d d d d d h h h h"
PLAYER_STATE = 11

GAME_STATE = 51
# | player own id | player count |
GAME_STATE_FORMAT = "i i " # + n player states
