from statemachine import State

class Menu(State):
    def __init__(self, stateMachine):
        super().__init__(stateMachine)

    def initialize(self):
        pass

    def start(self):
        nick = input("Nickname: ")
        ip = input("Server IP: ")
        self.stateMachine.goto("game", args = (nick, ip))
