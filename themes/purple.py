from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(25, 26, 33))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(248, 248, 242))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(25, 26, 33))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(248, 248, 242))
    palette.setColor(QPalette.ColorRole.Text, QColor(248, 248, 242))
    palette.setColor(QPalette.ColorRole.Button, QColor(68, 61, 90))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(241, 250, 140))

    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #f8f8f2;
        background-color: #282a36;
    }

    QGroupBox {
        border: 2px solid #6272a4;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #282a36;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #ffffff;
        font-weight: bold;
    }

    QListWidget, QTextEdit, QLineEdit {
        background-color: #282a36;
        color: #e0e0e0;
        border: 1px solid #404040;
        border-radius: 4px;
        padding: 0px;
        selection-background-color: #6272a4;
        selection-color: white;
    }

    QPushButton {
        background-color: #282a36;
        color: #fffbeb;
        border: 1px solid #6272a4;
        border-radius: 4px;
        padding: 8px 12px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #282a36;
        border-color: #bd93f9;
    }

    QPushButton:pressed {
        background-color: #282a36;
    }

    QPushButton:disabled {
        color: #777;
        background-color: #1f1f1f;
    }

    QMenuBar {
        background-color: #282a36;
        color: #ffffff;
        border-bottom: 1px solid #404040;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
    }

    QMenuBar::item:selected {
        background-color: #6272a4;
    }

    QMenu {
        background-color: #282a36;
        color: #f8f8f2;
        border: 1px solid #404040;
    }

    QMenu::item:selected {
        background-color: #6272a4;
    }

    QScrollBar:vertical {
        border: 1px solid #382750;
        background: #282a36;
        width: 15px;
        margin: 0;
    }

    QScrollBar:horizontal {
        border: 1px solid #382750;
        background: #282a36;
        width: 15px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: #7585b3;
        min-height: 20px;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background: #7585b3;
        min-width: 20px;
        border-radius: 7px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }

    QProgressBar {
        border: 1px solid #bd93f9;
        border-radius: 4px;
        text-align: center;
        background-color: #44475a;
    }

    QProgressBar::chunk {
        border-radius: 0px;
        background-color: #6272a4;
    }
    """)

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)
