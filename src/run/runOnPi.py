from core.userinput.SerialEspUserInput import SerialEspUserInput
from core.rendering.renderer.WS2812BRenderer import WS2812BRenderer
from games.pong.PongScene import PongScene
import Program

def start():
    Program.initalize(WS2812BRenderer(), SerialEspUserInput(), PongScene())
