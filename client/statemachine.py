

class statemachine():
    def __init__(self):
        self.state_in_call = False
        self.state_window_open = False
        self.state_calling = False

    def open_window(self):
        self.state_window_open = True
        # if window open -> exit
        # open window

    def close_window(self):
        self.state_in_call = False
        self.state_window_open = False
        # if window closed -> exit
        # if in call -> end call
        # close window

    def build_call(self):
        self.state_in_call = True
        self.state_calling = True

    def in_call(self):
        self.state_calling = False

    def disconnect_call(self):
        self.state_in_call = False
