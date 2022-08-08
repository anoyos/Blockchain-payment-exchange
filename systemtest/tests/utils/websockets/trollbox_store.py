import socketio


# Store that can be added as namespace to client, to collect emitted messages from socket.
class TrollboxStore(socketio.ClientNamespace):
    new_messages = []
    deleted_messages = []

    def on_connect(self):
        print("TrollboxStore is connected")

    def on_disconnect(self):
        print("TrollboxStore is disconnected")

    def on_trollbox_new_msg(self, data):
        print(f"TrollboxStore got new-message {data}")
        self.new_messages.append(data)

    def on_trollbox_del_msg(self, data):
        print(f"TrollboxStore got delete-message {data}")
        self.deleted_messages.append(data)
