# BOARD CONFIG
NUM_OF_THE_SAME_CARDS = 2
SIZE_OF_BOARD = 4
NUM_OF_CARDS = SIZE_OF_BOARD * SIZE_OF_BOARD

# CLIENT COMMANDS
C_SHOW = 'SHOW'  # SHOW X Y

# SERVER COMMANDS
S_START = 'START'  # <-- start game
S_HIT = 'HIT'
S_MISSED = 'MISSED'
S_POINTS = 'POINTS'  # POINTS num_of_point ex. POINTS 34
S_END = 'END'  # END POINTS
S_BOARD_SIZE = 'BOARD'
S_CARD = 'CARD'    # CARD name
S_ERROR = 'ERROR'  # <-- invalid command
S_OK = 'OK'

# POINTS
POINTS = 100
PENALTY_POINTS = 5
