import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt
from PyQt6.Qsci import QsciScintilla, QsciLexerMatlab
from PyQt6.QtGui import QColor, QFont, QPalette
import markdown2
import os

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend'))
sys.path.append(backend_path)

import checker


class SeaThemedGameScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ocean Explorer Coding Challenge")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set the main window background and font
        self.setStyleSheet("""
            QMainWindow {
                background-color: #E6F3F5;
                font-family: 'Open Sans', sans-serif;
            }
        """)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        self.STEPS = ["can_jellyfish_swim", "count_familiar_sharks", "fine_nemos_skyscraper", "open_treasure_chest"]
        self.step = 0
        
        # Question area (left side)
        question_widget = QWebEngineView()
        question_html = markdown2.markdown(self.question)
        question_widget.setHtml(f"""
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
                    }}
                </style>
            </head>
            <body>{question_html}</body>
            </html>
        """)
        
        # Text editor (right side)
        self.editor = QsciScintilla()
        self.editor.setUtf8(True)
        lexer = QsciLexerMatlab()
        lexer.setDefaultColor(QColor("#00008B"))  # Dark blue text
        lexer.setDefaultPaper(QColor("#FFFFFF"))  # White background
        lexer.setDefaultFont(QFont("Consolas", 12))  # Using Consolas for code
        self.editor.setLexer(lexer)
        self.editor.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.editor.setMarginWidth(0, "000")
        self.editor.setMarginsForegroundColor(QColor("#00008B"))  # Dark blue
        self.editor.setMarginsBackgroundColor(QColor("#E0FFFF"))  # Light cyan
        self.editor.setCaretForegroundColor(QColor("#00008B"))
        self.editor.setIndentationGuides(True)
        self.editor.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.editor.setTabWidth(4)
        self.editor.setAutoIndent(True)
        
        # Set colors for sea theme
        self.editor.setPaper(QColor("#FFFFFF"))  # White background
        self.editor.setColor(QColor("#00008B"))  # Dark blue text
        
        # Set selection colors
        self.editor.setSelectionBackgroundColor(QColor("#4682B4"))  # Steel blue for selection
        self.editor.setSelectionForegroundColor(QColor("#FFFFFF"))  # White text for selection
        
        # Feedback area
        self.feedback_area = QTextEdit()
        self.feedback_area.setReadOnly(True)
        self.feedback_area.setStyleSheet("""
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
        self.feedback_area.setHtml('<p style="font-weight: bold; font-size: 18px;">Set sail when you\'re ready, captain!</p>')
        
        # Submit button
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
        
        # Layout setup
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.editor, 12)
        
        feedback_and_submit = QHBoxLayout()
        feedback_and_submit.addWidget(self.feedback_area, 1)
        feedback_and_submit.addWidget(submit_button, 1)
        
        right_layout.addLayout(feedback_and_submit, 1)
        
        main_layout.addWidget(question_widget, 5)
        main_layout.addLayout(right_layout, 4)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def on_submit(self):
        submitted_text = self.editor.text()
        if checker.grade_matlab_function(self.STEPS[self.step], submitted_text.strip())[0]:
            self.feedback_area.setHtml(f'<p style="font-weight: bold; font-size: 18px;">Amazing! Puzzle piece is <i>"{self.next_piece}"</i></p>')
        else:
            self.feedback_area.setHtml('<p style="font-weight: bold; font-size: 18px;">No! Your solution isn\'t quite right yet.</p>')

    # These properties would be set when initializing the class
    @property
    def question(self):
        return checker.fetch_question(self.STEPS[self.step])

    @property
    def next_piece(self):
        return self.STEPS[self.step+1] if self.step+1 < len(self.STEPS) else "END"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SeaThemedGameScreen()
    window.show()
    sys.exit(app.exec())
