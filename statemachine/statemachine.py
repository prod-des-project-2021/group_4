from .state import State

class StateMachine:
    def __init__(self):
        self.states = dict()

    # method for registering a new state
    # states must be subclasses of statemachine.State
    def register(self, name, className):
        if(issubclass(className, State)):
            self.states[name] = className(self)
        else:
            raise Exception("State Machine class must be subclass of statemachine.State")

    # method for moving to another state
    # statemachine.state can use it directly from self
    def goto(self, name, args = None):
        if(name in self.states):
            if(args != None):
                self.states[name].initialize(*args)
            else:
                self.states[name].initialize()
            self.states[name].start()
        else:
            raise Exception("State "+str(name)+" is not registered")

    # method for going to another state without initializing it first
    # WARNING: misuse may produce unexpected bugs!
    def gono(self, name):
        if(name in self.states):
            self.states[name].start()
        else:
            raise Exception("State "+str(name)+" is not registered")

    # method for refreshing any given state
    def refresh(self, name):
        self.states[name].refresh()
