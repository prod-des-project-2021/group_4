from .formats import *
from .playerstate import *

# raw: raw packet
# returns a list of players
def gamestate_unpack(raw):
    player_count_flag = struct.unpack_from(GAME_STATE_FORMAT, raw, 0)
    players = list()

    player_size = struct.calcsize(PLAYER_STATE_FORMAT)
    front_padding = struct.calcsize(GAME_STATE_FORMAT)

    for i in range(0, player_count_flag[0]):
        player = playerstate_unpack(raw[(front_padding+i*player_size):front_padding+player_size+i*player_size])
        players.append(player)

    return players 

# players: list of players
# returns list encoded in bytes
def gamestate_pack(players):
    player_count = len(players)

    # getting a copy of gamestate format
    gamestate_format = str(GAME_STATE_FORMAT)

    # reserving bytes for player states
    gamestate_format = gamestate_format + str(player_count*struct.calcsize(PLAYER_STATE_FORMAT))+"s"

    player_bytes = bytes()
    for player in players:
        player_packed = playerstate_pack(player)
        player_bytes = player_bytes + player_packed

    packed = struct.pack(gamestate_format,
        player_count,
        player_bytes
    )

    return packed
