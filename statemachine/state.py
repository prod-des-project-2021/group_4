class State:
    def __init__(self, stateMachine):
        self.stateMachine = stateMachine # get a handle to statemachine

    def initialize(self):
        pass

    def refresh(self):
        self.initialize()

    def start(self):
        pass

    # method for moving to another state from state
    def goto(self, name, args = None):
        if(args != None):
            self.stateMachine.goto(name, args)
        else:
            self.stateMachine.goto(name)

    # method for moving to another state without initializing
    def gono(self, name):
        self.stateMachine.gono(name)
