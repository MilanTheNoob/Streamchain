from enum import Enum

class Verbosity(Enum): # Enum "Verbosity" is used not just for verbosity, but also to enable debug features (auto saving during mining, etc.)
    NORMAL=1
    VERBOSE=2
    SUPER_VERBOSE=3