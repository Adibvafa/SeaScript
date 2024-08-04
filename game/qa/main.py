import sys
import os

# Adjust the paths to import the MatlabGrader class and setup function
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
backend_path = os.path.join(project_root, 'backend')

sys.path.append(project_root)
sys.path.append(backend_path)

from setup import setup_resources
from checker import MatlabGrader

# Rest of the imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.Qsci import QsciScintilla, QsciLexerMatlab
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt, QTimer
import markdown
import emoji

class SeaThemedGameScreen(QMainWindow):
    def __init__(self, matlab_grader, step=0):
        super().__init__()
        self.matlab_grader = matlab_grader
        self.STEPS = ["can_jellyfish_swim", "count_familiar_sharks", "find_nemos_skyscraper", "open_treasure_chest"]
        self.step = step
        self.current_question = self.fetch_question()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ocean Explorer")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #E8F5F7, stop:1 #B3E5FC);
                font-family: 'Segoe UI', sans-serif;
            }
        """)

        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setSpacing(11)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(11)
        right_layout = QVBoxLayout()
        right_layout.setSpacing(11)

        self.challenge_title = self.create_challenge_title()
        self.question_widget = self.create_question_widget()
        self.editor = self.setup_editor()
        self.feedback_area = self.create_feedback_area()
        button_layout = self.create_button_layout()

        left_layout.addWidget(self.challenge_title)
        left_layout.addWidget(self.question_widget)

        right_layout.addWidget(self.editor)
        right_layout.addWidget(self.feedback_area)
        right_layout.addLayout(button_layout)

        main_layout.addLayout(left_layout, 55)
        main_layout.addLayout(right_layout, 45)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_challenge_title(self):
        title_label = QLabel()
        title_label.setStyleSheet("""
            QLabel {
                color: #006064;
                font-size: 24px;
                font-weight: bold;
                padding: 11px;
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 10px;
                max-height: 200px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return title_label

    def create_question_widget(self):
        question_widget = QWebEngineView()
        self.update_question_html(question_widget)
        return question_widget

    def update_question_html(self, widget):
        emoji_question = emoji.emojize(self.current_question, language='alias')
        md = markdown.Markdown(extensions=['codehilite', 'fenced_code'])
        question_html = md.convert(emoji_question)
        widget.setHtml(self.get_styled_html(question_html))

    def get_styled_html(self, content):
        # Extract the title (first line) from the content
        title, body = content.split('\n', 1)
        self.challenge_title.setText(title.strip())
        return f"""
            <html>
            <head>
                <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;700&display=swap" rel="stylesheet">
                <style>
                    body {{
                        font-family: 'Quicksand', sans-serif;
                        color: #00586B;
                        padding: 21px;
                        font-size: 20px;
                        background-color: rgba(255, 255, 255, 0.7);
                        border-radius: 15px;
                    }}
                    h1 {{
                        font-size: 30px;
                        color: #004D60;
                        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
                    }}
                    pre {{
                        background-color: #E0F7FA;
                        border-radius: 8px;
                        padding: 13px;
                        overflow-x: auto;
                        border: 1px solid #B2EBF2;
                    }}
                    code {{
                        font-family: 'Consolas', monospace;
                        font-size: 16px;
                    }}
                </style>
            </head>
            <body>{body}</body>
            </html>
        """

    def setup_editor(self):
        editor = QsciScintilla()
        editor.setUtf8(True)
        lexer = QsciLexerMatlab()
        self.configure_lexer(lexer)
        editor.setLexer(lexer)
        self.configure_editor(editor)
        return editor

    def configure_lexer(self, lexer):
        lexer.setDefaultColor(QColor("#00586B"))
        lexer.setDefaultPaper(QColor("#FFFFFF"))
        lexer.setDefaultFont(QFont("Consolas", 12))

    def configure_editor(self, editor):
        editor.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        editor.setMarginWidth(0, "000")
        editor.setMarginsForegroundColor(QColor("#006064"))
        editor.setMarginsBackgroundColor(QColor("#E0F7FA"))
        editor.setCaretForegroundColor(QColor("#00586B"))
        editor.setIndentationGuides(True)
        editor.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        editor.setTabWidth(4)
        editor.setAutoIndent(True)
        editor.setPaper(QColor("#FFFFFF"))
        editor.setColor(QColor("#00586B"))
        editor.setSelectionBackgroundColor(QColor("#B2EBF2"))
        editor.setSelectionForegroundColor(QColor("#00586B"))

    def create_feedback_area(self):
        feedback_area = QTextEdit()
        feedback_area.setReadOnly(True)
        feedback_area.setStyleSheet("""
            QTextEdit {
                background-color: rgba(224, 247, 250, 0.7);
                color: #006064;
                border: 2px solid #4DD0E1;
                border-radius: 15px;
                padding: 11px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 20px;
                max-height: 50px;
            }
        """)
        feedback_area.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        feedback_area.setHtml('<p style="margin: 0; font-weight: bold; font-size: 20px;">Ready, captain?</p>')
        return feedback_area

    def create_button_layout(self):
        button_layout = QHBoxLayout()
        button_layout.setSpacing(11)  # Reduced spacing between buttons

        set_sail_button = self.create_set_sail_button()
        reset_button = self.create_reset_button()

        button_layout.addWidget(set_sail_button)
        button_layout.addWidget(reset_button)

        return button_layout

    def create_set_sail_button(self):
        set_sail_button = QPushButton("Set Sail!")
        set_sail_button.setStyleSheet("""
            QPushButton {
                background-color: #006D75;
                max-width: 250px;
                min-height: 50px;
                color: white;
                border: none;
                text-align: center;
                text-decoration: none;
                font-size: 24px;
                margin: 10px 0;
                border-radius: 25px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #006064;
            }
        """)
        set_sail_button.clicked.connect(self.on_submit)
        return set_sail_button

    def create_reset_button(self):
        reset_button = QPushButton("Reset")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #0097A7;
                min-height: 50px;
                max-width: 250px;
                color: white;
                border: none;
                text-align: center;
                text-decoration: none;
                font-size: 24px;
                margin: 10px 0;
                border-radius: 25px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #00838F;
            }
        """)
        reset_button.clicked.connect(self.reset_editor)
        return reset_button

    def reset_editor(self):
        self.editor.clear()
        self.feedback_area.setHtml('<p style="margin: 0; font-weight: bold; font-size: 20px;">Editor cleared. Ready for a fresh start!</p>')

    def on_submit(self):
        self.feedback_area.setHtml('<p style="margin: 0; font-weight: bold; font-size: 20px;">Hold on tight! Checking your code...</p>')
        QApplication.processEvents()
        QTimer.singleShot(500, self.perform_check)

    def perform_check(self):
        submitted_text = self.editor.text()
        all_correct, _ = self.matlab_grader.grade_matlab_function(self.STEPS[self.step], submitted_text.strip())
        if all_correct:
            self.feedback_area.setHtml(f'<p style="margin: 0; font-weight: bold; font-size: 20px;">Wonderful! Puzzle piece is: <strong><em>"{self.next_piece}"</em></strong></p>')
        else:
            self.feedback_area.setHtml('<p style="margin: 0; font-weight: bold; font-size: 20px;">Not quite right. Try again!</p>')

    def fetch_question(self):
        return self.matlab_grader.fetch_question(self.STEPS[self.step])

    @property
    def next_piece(self):
        return self.STEPS[self.step + 1] if self.step + 1 < len(self.STEPS) else "END"

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Initialize resources and create MatlabGrader instance
    matlab_engine, collection, mongo_client = setup_resources()
    grader = MatlabGrader(matlab_engine, collection, mongo_client)

    # Create and show the main window
    window = SeaThemedGameScreen(grader, step=0)
    window.show()

    # Run the application
    exit_code = app.exec()

    # Clean up resources
    grader.close_resources()

    sys.exit(exit_code)