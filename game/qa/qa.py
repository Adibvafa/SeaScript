import sys
from typing import Callable

from PyQt6.QtWidgets import QApplication

from backend.checker import MatlabGrader
from game.qa.main import SeaThemedGameScreen
from setup import setup_resources

window: SeaThemedGameScreen
completed_challenges = set()
app = QApplication(sys.argv)

def init_qa():
    # Initialize resources and create MatlabGrader instance
    matlab_engine, collection, mongo_client = setup_resources()

    # Set up the grader
    global grader
    grader = MatlabGrader(matlab_engine, collection, mongo_client)


def _on_complete(other_callback: Callable, step: int):
    global completed_challenges
    completed_challenges.add(step)
    other_callback()


def open_challenge(step: int, callback: Callable):
    window = SeaThemedGameScreen(grader, step=step)
    window.update_question_html(window.question_widget)
    window.show()
    window.callback = lambda: _on_complete(callback, step)
    app.exec()