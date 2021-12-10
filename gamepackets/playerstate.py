import struct
from .formats import *

def playerstate_pack(player):
    packed = struct.pack(PLAYER_STATE_FORMAT,
        player.id,
        player.position.x,
        player.position.y,
        player.angle,
        player.velocity.x,
        player.velocity.y,
        player.health,
        player.accelerating,
        player.shooting,
        player.alive
    )
    return packed

def playerstate_unpack(raw):
    unpacked = struct.unpack(PLAYER_STATE_FORMAT, raw)
    data = {
        "id":           unpacked[0],
        "position.x":   unpacked[1],
        "position.y":   unpacked[2],
        "angle":        unpacked[3],
        "velocity.x":   unpacked[4],
        "velocity.y":   unpacked[5],
        "health":       unpacked[6],
        "accelerating": unpacked[7],
        "shooting":     unpacked[8],
        "alive":        unpacked[9]
    }
    return data
