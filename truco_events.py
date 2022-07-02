from enum import IntEnum

class TrucoEvents(IntEnum):
    GAME_STARTED      = 0
    ROUND_STARTED     = 1
    ROUND_PREPARED    = 2
    RAN_TRUCO_SESSION = 3
    ROUND_RESOLVED    = 4
    ROUND_ENDED       = 5
    GAME_ENDED        = 6
