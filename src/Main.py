#!/usr/bin/env python3

import sys
import os
import pydevd

# Start up the engine, given that the
#   current standard output is not piped.
if not sys.stdin.isatty():
    print("Oomph, I can not be run from a piped output. Please run directly from a terminal.")

    os.system('start bash.exe -c Main.py')
    input("Program is stopping...")
else:
    from Engine import Engine
    from Scenes.Menu.MenuScene import MenuScene
    from Window import Window

    # Start debugging
    pydevd.settrace('localhost', port=34564, stdoutToServer=False, stderrToServer=True)
    os.environ['TERM'] = 'xterm'  # Fix Pydev breaking stuff, fuck you pydevd

    # Create the environment for our game
    window = Window(100, 100)
    engine = Engine(window)

    engine.scene = MenuScene()

    engine.start()
    window.exit()
