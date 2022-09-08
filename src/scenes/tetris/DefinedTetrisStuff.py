
from config import Colors
from games.tetris.Shape import Shape

BACKGROUND_COLOR = Colors.OFF

GAME_OVER_COLOR = Colors.WHITE
O_block_color = Colors.YELLOW
I_block_color = Colors.CYAN
J_block_color = Colors.DARK_BLUE
L_block_color = Colors.ORANGE
S_block_color = Colors.GREEN
Z_block_color = Colors.RED
T_block_color = Colors.PURPLE

# Predefined shapes for the tetris blocks (With their colors)
DEFINED_SHAPES = (
    Shape([[0, 0], [1, 0], [0, -1], [1, -1]], O_block_color),
    Shape([[-1, 0], [0, 0], [1, 0], [2, 0]], I_block_color),
    Shape([[-1, -1], [-1, 0], [0, 0], [1, 0]], J_block_color),
    Shape([[-1, 0], [0, 0], [1, 0], [1, -1]], L_block_color),
    Shape([[-1, 0], [0, 0], [0, -1], [1, -1]], S_block_color),
    Shape([[-1, -1], [0, -1], [0, 0], [1, 0]], Z_block_color),
    Shape([[-1, 0], [0, 0], [0, -1], [1, 0]], T_block_color),
)