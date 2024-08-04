import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.Qsci import QsciScintilla, QsciLexerMatlab
from PyQt6.QtGui import QColor, QFont
import markdown
import emoji

# Adjust the path to import the checker module
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend'))
sys.path.append(backend_path)
import checker

class SeaThemedGameScreen(QMainWindow):
    def __init__(self, step=0):
        super().__init__()
        self.STEPS = ["can_jellyfish_swim", "count_familiar_sharks", "find_nemos_skyscraper", "open_treasure_chest"]
        self.step = step
        self.current_question = self.fetch_question()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ocean Explorer Coding Challenge")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #E6F3F5;
                font-family: 'Open Sans', sans-serif;
            }
        """)

        main_widget = QWidget()
        main_layout = QHBoxLayout()

        self.question_widget = self.create_question_widget()
        editor_layout = self.create_editor_layout()

        main_layout.addWidget(self.question_widget, 1)
        main_layout.addLayout(editor_layout, 1)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_question_widget(self):
        question_widget = QWebEngineView()
        self.update_question_html(question_widget)
        return question_widget

    def update_question_html(self, widget):
        # Convert emojis in the question text
        emoji_question = emoji.emojize(self.current_question, language='alias')
        
        # Use the Python-Markdown library with codehilite extension
        md = markdown.Markdown(extensions=['codehilite', 'fenced_code'])
        question_html = md.convert(emoji_question)
        
        widget.setHtml(self.get_styled_html(question_html))

    def get_styled_html(self, content):
        return f"""
            <html>
            <head>
                <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap" rel="stylesheet">
                <style>
                    body {{
                        font-family: 'Open Sans', sans-serif;
                        color: #00008B;
                        padding: 20px;
                        font-size: 18px;
                    }}
                    h1 {{
                        font-size: 28px;
                        color: #006994;
                        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
                    }}
                    pre {{
                        background-color: #B0E0E6;
                        border-radius: 5px;
                        padding: 10px;
                        overflow-x: auto;
                    }}
                    code {{
                        font-family: 'Consolas', monospace;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>{content}</body>
            </html>
        """

    def create_editor_layout(self):
        layout = QVBoxLayout()
        self.editor = self.setup_editor()
        self.feedback_area = self.create_feedback_area()
        submit_button = self.create_submit_button()

        layout.addWidget(self.editor, 12)

        feedback_and_submit = QHBoxLayout()
        feedback_and_submit.addWidget(self.feedback_area, 1)
        feedback_and_submit.addWidget(submit_button, 1)

        layout.addLayout(feedback_and_submit, 1)
        return layout

    def setup_editor(self):
        editor = QsciScintilla()
        editor.setUtf8(True)
        lexer = QsciLexerMatlab()
        self.configure_lexer(lexer)
        editor.setLexer(lexer)
        self.configure_editor(editor)
        return editor

    def configure_lexer(self, lexer):
        lexer.setDefaultColor(QColor("#00008B"))
        lexer.setDefaultPaper(QColor("#FFFFFF"))
        lexer.setDefaultFont(QFont("Consolas", 12))

    def configure_editor(self, editor):
        editor.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        editor.setMarginWidth(0, "000")
        editor.setMarginsForegroundColor(QColor("#00008B"))
        editor.setMarginsBackgroundColor(QColor("#E0FFFF"))
        editor.setCaretForegroundColor(QColor("#00008B"))
        editor.setIndentationGuides(True)
        editor.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        editor.setTabWidth(4)
        editor.setAutoIndent(True)
        editor.setPaper(QColor("#FFFFFF"))
        editor.setColor(QColor("#00008B"))
        editor.setSelectionBackgroundColor(QColor("#4682B4"))
        editor.setSelectionForegroundColor(QColor("#FFFFFF"))

    def create_feedback_area(self):
        feedback_area = QTextEdit()
        feedback_area.setReadOnly(True)
        feedback_area.setStyleSheet("""
            QTextEdit {
                background-color: #E0FFFF;
                color: #00008B;
                border: 1px solid #4682B4;
                border-radius: 10px;
                padding: 5px;
                font-family: 'Open Sans', sans-serif;
                font-size: 22px;
                max-height: 40px;
            }
        """)
        feedback_area.setHtml('<p style="font-weight: bold; font-size: 18px;">Set sail when you\'re ready, captain!</p>')
        return feedback_area

    def create_submit_button(self):
        submit_button = QPushButton("Set Sail!")
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #20B2AA;
                max-width: 100px;
                padding: 12px;
                color: white;
                border: none;
                text-align: center;
                text-decoration: none;
                font-size: 20px;
                margin: 0px 0;
                border-radius: 10px;
                font-family: 'Open Sans', sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #48D1CC;
            }
        """)
        submit_button.clicked.connect(self.on_submit)
        return submit_button

    def on_submit(self):
        self.feedback_area.setHtml('<p style="font-weight: bold; font-size: 18px;">Alright, Let\'s see...</p>')
        submitted_text = self.editor.text()
        if checker.grade_matlab_function(self.STEPS[self.step], submitted_text.strip())[0]:
            self.feedback_area.setHtml(f'<p style="font-weight: bold; font-size: 18px;">Amazing! Puzzle piece is <i>"{self.next_piece}"</i></p>')
        else:
            self.feedback_area.setHtml('<p style="font-weight: bold; font-size: 18px;">No! Your solution isn\'t quite right yet.</p>')

    def fetch_question(self):
        return checker.fetch_question(self.STEPS[self.step])

    @property
    def next_piece(self):
        return self.STEPS[self.step + 1] if self.step + 1 < len(self.STEPS) else "END"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SeaThemedGameScreen(step=0)
    window.show()
    sys.exit(app.exec())