import threading


class InputThread(threading.Thread):
    user_input = ""
    last_user_input = ""

    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input

    def run(self):
        self.daemon = True
        while True:
            self.last_user_input = input(f"{self.user_input}")
