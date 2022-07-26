from core.userinput.DummyUserInput import DummyUserInput
from core.rendering.renderer.PyGameRenderer import PyGameRenderer
from core.rendering.Screen import Screen
from run.start import start
from games.snake.Snake import Snake

start(PyGameRenderer(Screen(18, 20)), DummyUserInput(), Snake())