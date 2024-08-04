import sys
from typing import Callable

from PyQt6.QtWidgets import QApplication

from backend.checker import MatlabGrader
from game.qa.main import SeaThemedGameScreen
from setup import setup_resources

window: SeaThemedGameScreen
completed_challenges = []


def init_qa():
    app = QApplication(sys.argv)

    # Initialize resources and create MatlabGrader instance
    matlab_engine, collection, mongo_client = setup_resources()
    grader = MatlabGrader(matlab_engine, collection, mongo_client)

    # Create and show the main window
    global window
    window = SeaThemedGameScreen(grader, step=3)
    app.exec()


def _on_complete(other_callback: Callable):
    global completed_challenges
    completed_challenges.append(window.step)
    window.hide()
    other_callback()


def open_challenge(num: int, callback: Callable):
    window.step = num
    window.update_question_html(window.question_widget)
    window.show()
    window.callback = lambda: _on_complete(callback)
