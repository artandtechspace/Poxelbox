import json
import time

from core.rendering.renderer.BoxSchemaRendererBase import BoxSchemaRendererBase
import asyncio
from websockets.server import serve
import threading
from threading import Lock

# Packet-IDS
PKT_SET_COLOR = 1
PKT_SET_IDX = 0
PKT_INIT = 2
PKT_OPTIONAL_KEEP_ALIVE = 3

class RemoteRenderer(BoxSchemaRendererBase):

    def __init__(self):
        super().__init__()

        # Data to be parsed between the threads
        self.lock = Lock()

        # Led-state sending data
        self.do_push = False  # Flag:If the current new data should be sent to the display
        # {index: (red, green, blue)}
        self.led_state: {int: (int, int, int)} = {}  # The complete state of all leds to send if the display gets lost
        self.update_state: {int: (int, int, int)} = {}  # All new updates after a push
        self.last_color: int = 0  # The last color (as hex-format) that was send to the display

        # If there is already a client connected
        self.has_connection = False

        # Creates the new thread
        p = threading.Thread(target=self.thread_start, daemon=True)
        p.start()

    def setup(self):
        super().setup()

    def thread_start(self):
        """ Runs as the main method of the render-thread """
        asyncio.run(self.main())

    async def main(self):
        """The main method for the async-io of the render-thread"""
        # Runs the websocket-server until the application closes
        async with serve(lambda ws: self.on_client_connect(ws), "localhost", 8765):
            await asyncio.Future()  # run forever

    async def on_client_connect(self, websocket):
        """Method that is used to handle ever client that connects"""

        # Checks if there is already a client connected
        if self.has_connection:
            await websocket.close()
            print("Got a second display that got closed")
            return

        # Blocks any other clients from connecting
        self.has_connection = True

        # Resets some initial values
        self.last_color = 0

        print("Display connected")
        try:
            # Sends the amount of leds connected
            await websocket.send(self.create_init_packet())

            # Thread-safety
            self.lock.acquire()

            # Converts the complete led state to a packet to give the display the initial setup
            pkt, color = self.convert_to_packet(self.led_state, self.last_color)
            self.last_color = color
            await websocket.send(pkt)
            self.lock.release()

            # Time when the last update got send
            update_time = time.time()+1

            while True:
                # Ensures a small timeout
                await asyncio.sleep(0.05)

                # Thread-safety
                self.lock.acquire()

                # Checks if the leds should be pushed
                if self.do_push:
                    # Pushes the leds
                    self.do_push = False
                    # Copies and clears the state-update array to ensure that
                    # the game-thread can run while the data is being sent
                    update = self.update_state.copy()
                    self.update_state.clear()
                    # Thread-safety
                    self.lock.release()
                    # Sends the actual message
                    pkt, color = self.convert_to_packet(update, self.last_color)
                    self.last_color = color
                    await websocket.send(pkt)

                    # Resets the update time
                    update_time = time.time()+1
                else:
                    # Thread-safety
                    self.lock.release()

                    # Sends an optional keep alive if the time has been reached
                    if time.time() > update_time:
                        await websocket.send(bytearray([PKT_OPTIONAL_KEEP_ALIVE]))

                        # Resets the update time
                        update_time = time.time() + 1
        except Exception as e:
            print("Display disconnected ", e)
            # Client has disconnected, releasing the has-connection flag
            self.has_connection = False

    def create_init_packet(self):
        """Creates an init-packet"""

        # Gets the screen-length (Amount of leds)
        size = self.screen.size_x * self.screen.size_y * 3 * 4

        # Splits it into 2 bytes
        b1 = size & 0xff
        b2 = (size >> 8) & 0xff

        return bytearray([
            PKT_INIT,
            b1, b2
        ])

    def create_set_color_packet(self, clr: int):
        """Creates a color-set-packet"""
        return bytearray([
            PKT_SET_COLOR,
            clr & 0xff,  # red
            (clr >> 8) & 0xff,  # green
            (clr >> 16) & 0xff  # blue
        ])

    def create_set_index_packet(self, idx: int):
        """Creates an index-set packet to set a specific led to the previously selected color"""
        # Splits the index into two bytes to support more than 255 pixel
        b1 = idx & 0xff
        b2 = (idx >> 8) & 0xff

        return bytearray([
            PKT_SET_IDX,
            b1,
            b2
        ])

    def convert_to_packet(self, clrs: {int: (int, int, int)}, initial_color: int):
        """Takes in multiple color-updates and the color that is currently set at the client and converts them to the
        smallest packet possible. Also it returns a new initial_color, which now the client will have after the packet"""

        # Colors mappings {hex-color: [led-indexes]}
        mapping: {int: [int]} = {}

        # Iterates over all entry's
        for idx in clrs:
            raw = clrs[idx]
            
            red = int(raw[0])
            green = int(raw[1])
            blue = int(raw[2])

            # Calculates the hex color
            hex_clr = red | (green << 8) | (blue << 16)

            # Appends the color to the mapping-array
            if hex_clr not in mapping:
                mapping[hex_clr] = []

            mapping[hex_clr].append(idx)

        # List with packets to send to the client
        pkt_list = []

        # Checks if the initial color is also used in these packets and if so sends those packets first
        # This allows us to skip color-packets
        if initial_color in mapping:
            # Creates "free" index packets as a color packet can be skipped
            for index in mapping[initial_color]:
                pkt_list.append(self.create_set_index_packet(index))

            # Removes the packets
            mapping[initial_color] = None

        for clr in mapping:
            indexes = mapping[clr]
            if indexes is None:
                continue
            # Creates the color-packet
            pkt_list.append(self.create_set_color_packet(clr))

            # Creates the data
            for idx in indexes:
                pkt_list.append(self.create_set_index_packet(idx))

            # Updates the new color
            initial_color = clr

        return pkt_list, initial_color

    def set_box_schema_led(self, idx: int, color: (int, int, int)):
        # Thread-safely updates the led
        self.lock.acquire()
        self.led_state[idx] = color
        self.update_state[idx] = color
        self.lock.release()

    def push_leds(self):
        # Thread-safely pushes the leds
        self.lock.acquire()
        self.do_push = True
        self.lock.release()
