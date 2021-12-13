from statemachine import State

class MainMenu(State):
    def __init__(self, stateMachine):
        super().__init__(stateMachine)

    def initialize(self, version):
        print(str(version))

    def start(self):
        print("Welcome to the game!")
        nick = input("Nickname: ")
        ip = input("Server IP: ")
        print("Joining server at "+str(ip)+"...")

        # done here, move to next state
        self.goto("game", args=(nick, ip))
