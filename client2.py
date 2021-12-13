from statemachine import StateMachine
from menu import Menu
from game import Game

def main():
    appState = StateMachine()
    appState.register("menu", Menu)
    appState.register("game", Game)
    appState.goto("menu")

if __name__ == '__main__':
    main()
