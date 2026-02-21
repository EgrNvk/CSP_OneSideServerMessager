

class ClientController:
    def __init__(self, view, client):
        self.view = view
        self.client = client


        self.running=False

    def start(self):
        try:
            self.client.connect()
        except:
            self.view.add_line("SYSTEM: Server offline")
            self.view.root.after(5000, self.start)
            return

        self.client.socket.setblocking(False)
        self.running = True
        self.view.add_line("CONNECTED TO SERVER")
        self.poll_receive()

    def poll_receive(self):
        try:
            msg=self.client.receive()
            if msg:
                self.view.add_line(msg)
        except:
            pass

        self.view.root.after(50, self.poll_receive)