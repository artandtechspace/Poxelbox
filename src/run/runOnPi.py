from core.userinput.SerialEspUserInput import SerialEspUserInput
from core.rendering.renderer.WS2812BRenderer import WS2812BRenderer
from scenes.LoadingScreenScene import LoadingScreen
import Program


def start():
    Program.initalize(WS2812BRenderer(), SerialEspUserInput(), LoadingScreen())
