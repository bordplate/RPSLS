#!/usr/bin/env python3

import sys

# Start up the engine, given that the
#   current standard output is not piped.
if not sys.stdin.isatty():
    print("Oomph, I can not be run from a piped output. Please run directly from a terminal.")
else:
    from Engine import Engine
    from Scenes.Menu.MenuScene import MenuScene
    from Window import Window

    # Create the environment for our game
    window = Window(100, 100)
    engine = Engine(window)

    engine.scene = MenuScene()

    engine.start()
    window.exit()
