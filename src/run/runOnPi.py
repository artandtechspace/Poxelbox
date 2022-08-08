from core.userinput.SerialEspUserInput import SerialEspUserInput
from core.rendering.renderer.ANSIRenderer import ANSIRenderer
from core.rendering.Screen import Screen
from games.pong.PongScene import PongScene
import Program

# TODO: Currently the WS2812B-Renderer is not existing, therefor the ANSI-Renderer is here

Program.initalize(ANSIRenderer(Screen(18, 24)), SerialEspUserInput(), PongScene())