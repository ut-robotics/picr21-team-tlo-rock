from enum import IntEnum
class State(IntEnum):
    stopped = 0
    automatic = 1
    remote = 2
class GameState(IntEnum):
    searching = 0
    moveto = 1
    orbit = 2
    launch = 3