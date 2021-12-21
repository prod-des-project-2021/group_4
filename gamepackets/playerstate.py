import struct
from .formats import *

def playerstate_pack(player):
    packed = struct.pack(PLAYER_STATE_FORMAT,
        player.id,
        bytes(player.nickname, 'utf-8'),
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
        "nickname":     unpacked[1].decode("utf-8"),
        "position.x":   unpacked[2],
        "position.y":   unpacked[3],
        "angle":        unpacked[4],
        "velocity.x":   unpacked[5],
        "velocity.y":   unpacked[6],
        "health":       unpacked[7],
        "accelerating": unpacked[8],
        "shooting":     unpacked[9],
        "alive":        unpacked[10]
    }
    return data
