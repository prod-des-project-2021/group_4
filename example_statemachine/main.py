from statemachine import StateMachine
from statemachine import State
from mainmenu import MainMenu
from game import Game

def main():
    appState = StateMachine()
    appState.register("mainmenu", MainMenu)
    appState.register("game", Game)
    appState.goto("mainmenu", args=('SpaceGame 1.0 Beta',))

if __name__ == '__main__':
    main()
