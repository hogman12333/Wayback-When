from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


def apply(app, widget):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(255, 250, 220))  # Very light pastel yellow
    palette.setColor(QPalette.ColorRole.WindowText, QColor(70, 65, 50))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 253, 240))  # Almost white with yellow tint
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(250, 245, 220))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 253, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(70, 65, 50))
    palette.setColor(QPalette.ColorRole.Text, QColor(60, 55, 40))
    palette.setColor(QPalette.ColorRole.Button, QColor(255, 245, 200))  # Light pastel yellow
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(80, 75, 60))
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.darkYellow)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(255, 230, 150))  # Soft yellow highlight
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(50, 45, 30))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(180, 175, 150))

    app.setPalette(palette)

    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #464232;
        background-color: #fffadc;
    }

    QGroupBox { 
        border: 2px solid #e0d8b0;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #fffadc;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #8c7d32;
        font-weight: bold;
    }

    QListWidget, QTextEdit, QLineEdit {
        background-color: #fffef0;
        color: #464232;
        border: 1px solid #d8d0a0;
        border-radius: 4px;
        padding: 5px;
        selection-background-color: #ffe89c;
        selection-color: #464232;
    }

    QPushButton {
        background-color: #fff5c8;
        color: #464232;
        border: 1px solid #d8d0a0;
        border-radius: 4px;
        padding: 8px 12px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #fff0b4;
        border-color: #c0b070;
    }

    QPushButton:pressed {
        background-color: #e8e0b0;
    }

    QPushButton:disabled {
        color: #a09a82;
        background-color: #f0ead8;
    }

    QMenuBar {
        background-color: #fff5c8;
        color: #464232;
        border-bottom: 1px solid #d8d0a0;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
    }

    QMenuBar::item:selected {
        background-color: #ffe89c;
    }

    QMenu {
        background-color: #fffef0;
        color: #464232;
        border: 1px solid #d8d0a0;
    }

    QMenu::item:selected {
        background-color: #ffe89c;
    }

    QScrollBar:vertical {
        border: 1px solid #d8d0a0;
        background: #fffef0;
        width: 15px;
        margin: 0;
    }

    QScrollBar:horizontal {
        border: 1px solid #d8d0a0;
        background: #fffef0;
        height: 15px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: #e8e0b0;
        min-height: 20px;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background: #e8e0b0;
        min-width: 20px;
        border-radius: 7px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }

    QProgressBar {
        border: 1px solid #d8d0a0;
        border-radius: 4px;
        text-align: center;
        background-color: #fffef0;
    }

    QProgressBar::chunk {
        background-color: #ffdb58;  # Pastel yellow
        border-radius: 0px;
    }
    """)

    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)