import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt
from PyQt6.Qsci import QsciScintilla, QsciLexerMatlab
from PyQt6.QtGui import QColor, QFont, QPalette
import markdown2

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
        right_layout.addWidget(self.editor, 10)
        
        feedback_and_submit = QHBoxLayout()
        feedback_and_submit.addWidget(self.feedback_area, 1)
        feedback_and_submit.addWidget(submit_button, 1)
        
        right_layout.addLayout(feedback_and_submit, 1)
        
        main_layout.addWidget(question_widget, 1)
        main_layout.addLayout(right_layout, 1)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def on_submit(self):
        submitted_text = self.editor.text()
        if submitted_text.strip() == self.answer:
            self.feedback_area.setHtml(f'<p style="font-weight: bold; font-size: 18px;">Nice job! Your next puzzle piece is <i>"{self.next_piece}"</i></p>')
        else:
            self.feedback_area.setHtml('<p style="font-weight: bold; font-size: 18px;">Try again. Your solution isn\'t quite right yet.</p>')

    # These properties would be set when initializing the class
    @property
    def question(self):
        return """# Jellyfish Swimming Hours\nDid you know? Some jellyfish species can't swim at night because they rely on visual cues to navigate. Let's help our gelatinous friends figure out when they can take a dip!\n## Your Mission\nWrite a MATLAB function `can_jellyfish_swim(hour)` that determines if our jellyfish can swim based on the hour of the day.\n### Function Specifications:\n- Input: `hour` (0-23, representing 24-hour time)\n- Output: 1 if the jellyfish can swim, 0 if it can't\n- Assume jellyfish can swim from 6:00 AM to 6:00 PM (hours 6 to 18 inclusive)\n### Example:
        >> can_jellyfish_swim(12)
        ans = 1  % Noon? Swim time!\n
        >> can_jellyfish_swim(22)
        ans = 0  % 10 PM? Better rest those tentacles.
        """

    @property
    def answer(self):
        return "A"

    @property
    def next_piece(self):
        return "MAMAAAA"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SeaThemedGameScreen()
    window.show()
    sys.exit(app.exec())