from core.userinput.DummyUserInput import DummyUserInput
from core.rendering.renderer.PyGameRenderer import PyGameRenderer
from core.rendering.Screen import Screen
from run.start import start

start(PyGameRenderer(Screen(18, 20)), DummyUserInput())