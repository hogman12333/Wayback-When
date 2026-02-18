from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(20, 30, 40))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 230, 240))
    palette.setColor(QPalette.ColorRole.Base, QColor(15, 25, 35))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(25, 35, 45))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(220, 230, 240))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 230, 240))
    palette.setColor(QPalette.ColorRole.Text, QColor(220, 230, 240))
    palette.setColor(QPalette.ColorRole.Button, QColor(35, 45, 55))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 230, 240))
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.cyan)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 150, 220))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(127, 147, 167))

    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #dce6f0;
        background-color: #141e28;
    }

    QGroupBox { 
        border: 2px solid #0d141a;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #141e28;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #c8d8e8;
        font-weight: bold;
    }

    QListWidget, QTextEdit, QLineEdit {
        background-color: #1d2d3d;
        color: #dce6f0;
        border: 1px solid #304050;
        border-radius: 4px;
        padding: 0px;
        selection-background-color: #3a5a7a;
        selection-color: white;
    }

    QPushButton {
        background-color: #253545;
        color: #dce6f0;
        border: 1px solid #304050;
        border-radius: 4px;
        padding: 8px 12px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #2d3d4d;
        border-color: #00bfff;
    }

    QPushButton:pressed {
        background-color: #141e28;
    }

    QPushButton:disabled {
        color: #6a7a8a;
        background-color: #1d2d3d;
    }

    QMenuBar {
        background-color: #1a2632;
        color: #dce6f0;
        border-bottom: 1px solid #304050;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
    }

    QMenuBar::item:selected {
        background-color: #2d3d4d;
    }

    QMenu {
        background-color: #1d2d3d;
        color: #dce6f0;
        border: 1px solid #304050;
    }

    QMenu::item:selected {
        background-color: #2d3d4d;
    }

    QScrollBar:vertical {
        border: 1px solid #2a4a6a;
        background: #1d2d3d;
        width: 15px;
        margin: 0;
    }

    QScrollBar:horizontal {
        border: 1px solid #304050;
        background: #1d2d3d;
        height: 15px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: #2d3d4d;
        min-height: 20px;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background: #2d3d4d;
        min-width: 20px;
        border-radius: 7px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }

    QProgressBar {
        border: 1px solid #304050;
        border-radius: 4px;
        text-align: center;
        background-color: #1d2d3d;
    }

    QProgressBar::chunk {
        background-color: #0096dc;
        border-radius: 0px;
    }
    """)
