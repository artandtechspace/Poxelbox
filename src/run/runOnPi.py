from core.userinput.SerialEspUserInput import SerialEspUserInput
from core.rendering.renderer.ANSIRenderer import ANSIRenderer
from core.rendering.Screen import Screen
from run.start import start
from games.pong.Pong import Pong

# TODO: Currently the WS2812B-Renderer is not existing, therefor the ANSI-Renderer is here
start(ANSIRenderer(Screen(18, 24)), SerialEspUserInput(), Pong())