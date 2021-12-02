# raw: raw packet
# returns a list of players
def gamestate_unpack(raw):
    pass

# players: list of players
# returns list encoded in bytes
def gamestate_pack(players):
    p_count = len(players)
    # ID, X, Y, Angle, Accelerating, Shooting
    p_format = "s d d d s s"
