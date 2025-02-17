# assuming a resulution of 1920 x 1080 = 16 : 9

# color scheme
BG_C    = '#FDF6E3'
GRID_C  = '#542437'
BLOCK_C = 'red'
PATH_C  = 'lightblue'
FINAL_C = 'blue'
START_C = '#C7F464'
GOAL_C  = 'yellow'

# grid size
START = (12, 12)
SIZE  = 25 # the nr of nodes=grid crossings in a row (or column)
GOAL  = (0, 0)

# pixel sizes
CELL  = 35 # size of cell/square in pixels
W  = (SIZE-1) * CELL # width of grid in pixels
H  = W # height of grid
TR = 10 # translate/move the grid, upper left is 10,10


