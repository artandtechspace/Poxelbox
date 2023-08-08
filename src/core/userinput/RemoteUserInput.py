from core.userinput.BaseUserInput import BaseUserInput
import asyncio
from websockets.server import serve
import threading
from threading import Lock


class RemoteUserInput(BaseUserInput):

    def __init__(self):
        super().__init__()

        # Key-status and player-id of player 1/2
        self.p1_status = 0b000000000
        self.p2_status = 0b000000001

        # Holds if the thread has changed p1 or p2 status
        self.p1_changed = False
        self.p2_changed = False

        # Data to be parsed between the threads
        self.lock = Lock()

        # If there is already a client connected
        self.has_connection = False

        # Creates the new thread
        p = threading.Thread(target=self.thread_start, daemon=True)
        p.start()

    def thread_start(self):
        """ Runs as the main method of the render-thread """
        asyncio.run(self.main())

    async def main(self):
        """The main method for the async-io of the render-thread"""
        # Runs the websocket-server until the application closes
        async with serve(lambda ws: self.on_client_connect(ws), "localhost", 8766):
            await asyncio.Future()  # run forever

    async def on_client_connect(self, websocket):
        """Method that is used to handle ever client that connects"""

        # Checks if there is already a client connected
        if self.has_connection:
            await websocket.close()
            print("Got a second input that got closed")
            return

        # Blocks any other clients from connecting
        self.has_connection = True

        # Resets some initial values
        self.p1_status = 0b000000000
        self.p2_status = 0b000000001

        print("Input connected")
        try:
            # Waits for data from
            async for msg in websocket:
                # Ensures the message is in byte format
                if not isinstance(msg, bytes):
                    continue

                # Ensures a correct length
                if len(msg) != 2:
                    continue

                # Builds the status and gets the player
                status = msg[0] | (msg[1] << 8)
                player_id = status & 1

                # Thread-safety
                self.lock.acquire()

                # Updates the data
                if player_id == 0:
                    self.p1_status = status
                    self.p1_changed = True
                else:
                    self.p2_status = status
                    self.p2_changed = True

                self.lock.release()
        except Exception as e:
            print("Connection reset", e)
            pass

        print("Input disconnected")
        # Client has disconnected, releasing the has-connection flag
        self.has_connection = False

    def update(self):

        # Temp-variable to store the data and perform any
        # actions without blocking the fetch-data-thread
        new_status = None

        # Thread-safety
        self.lock.acquire()
        # Checks if any input updated
        if self.p1_changed:
            new_status = self.p1_status
            self.p1_changed = False
        elif self.p2_changed:
            new_status = self.p2_status
            self.p2_changed = False
        self.lock.release()

        # If anything updated, forward that update
        if new_status is not None:
            self._on_change(new_status)