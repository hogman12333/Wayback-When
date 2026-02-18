from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


def apply(app, widget):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(40, 20, 30))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 220, 230))
    palette.setColor(QPalette.ColorRole.Base, QColor(35, 15, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 25, 35))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(240, 220, 230))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(240, 220, 230))
    palette.setColor(QPalette.ColorRole.Text, QColor(240, 220, 230))
    palette.setColor(QPalette.ColorRole.Button, QColor(55, 35, 45))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 220, 230))
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.magenta)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(220, 0, 150))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(167, 127, 147))

    app.setPalette(palette)

    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #f0dce6;
        background-color: #28141e;
    }

    QGroupBox { 
        border: 2px solid #1a0d14;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #28141e;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #e8c8d8;
        font-weight: bold;
    }

    QListWidget, QTextEdit, QLineEdit {
        background-color: #3d1d2d;
        color: #f0dce6;
        border: 1px solid #503040;
        border-radius: 4px;
        padding: 0px;
        selection-background-color: #7a3a5a;
        selection-color: white;
    }

    QPushButton {
        background-color: #452535;
        color: #f0dce6;
        border: 1px solid #503040;
        border-radius: 4px;
        padding: 8px 12px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #4d2d3d;
        border-color: #ff00bf;
    }

    QPushButton:pressed {
        background-color: #28141e;
    }

    QPushButton:disabled {
        color: #8a6a7a;
        background-color: #3d1d2d;
    }

    QMenuBar {
        background-color: #321a26;
        color: #f0dce6;
        border-bottom: 1px solid #503040;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
    }

    QMenuBar::item:selected {
        background-color: #4d2d3d;
    }

    QMenu {
        background-color: #3d1d2d;
        color: #f0dce6;
        border: 1px solid #503040;
    }

    QMenu::item:selected {
        background-color: #4d2d3d;
    }

    QScrollBar:vertical {
        border: 1px solid #6a2a4a;
        background: #3d1d2d;
        width: 15px;
        margin: 0;
    }

    QScrollBar:horizontal {
        border: 1px solid #503040;
        background: #3d1d2d;
        height: 15px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: #4d2d3d;
        min-height: 20px;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background: #4d2d3d;
        min-width: 20px;
        border-radius: 7px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }

    QProgressBar {
        border: 1px solid #503040;
        border-radius: 4px;
        text-align: center;
        background-color: #3d1d2d;
    }

    QProgressBar::chunk {
        background-color: #dc0096;
        border-radius: 0px;
    }
    """)

    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)