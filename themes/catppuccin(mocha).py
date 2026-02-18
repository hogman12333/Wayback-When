from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


def apply(app, widget):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 46))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(205, 214, 244))
    palette.setColor(QPalette.ColorRole.Base, QColor(24, 24, 37))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(30, 30, 46))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(24, 24, 37))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(205, 214, 244))
    palette.setColor(QPalette.ColorRole.Text, QColor(205, 214, 244))
    palette.setColor(QPalette.ColorRole.Button, QColor(49, 50, 68))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(205, 214, 244))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(166, 227, 161))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(137, 180, 250))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(24, 24, 37))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(127, 132, 156))

    app.setPalette(palette)

    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #cdd6f4;
        background-color: #1e1e2e;
    }

    QGroupBox { 
        border: 2px solid #181825;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #1e1e2e;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #bac2de;
        font-weight: bold;
    }

    QListWidget, QTextEdit, QLineEdit {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #45475a;
        border-radius: 4px;
        padding: 0px;
        selection-background-color: #585b70;
        selection-color: #cdd6f4;
    }

    QPushButton {
        background-color: #45475a;
        color: #cdd6f4;
        border: 1px solid #585b70;
        border-radius: 4px;
        padding: 8px 12px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #585b70;
        border-color: #89b4fa;
    }

    QPushButton:pressed {
        background-color: #1e1e2e;
    }

    QPushButton:disabled {
        color: #6c7086;
        background-color: #313244;
    }

    QMenuBar {
        background-color: #181825;
        color: #cdd6f4;
        border-bottom: 1px solid #45475a;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
    }

    QMenuBar::item:selected {
        background-color: #45475a;
    }

    QMenu {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #45475a;
    }

    QMenu::item:selected {
        background-color: #45475a;
    }

    QScrollBar:vertical {
        border: 1px solid #45475a;
        background: #313244;
        width: 15px;
        margin: 0;
    }

    QScrollBar:horizontal {
        border: 1px solid #45475a;
        background: #313244;
        height: 15px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: #585b70;
        min-height: 20px;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background: #585b70;
        min-width: 20px;
        border-radius: 7px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }

    QProgressBar {
        border: 1px solid #45475a;
        border-radius: 4px;
        text-align: center;
        background-color: #313244;
    }

    QProgressBar::chunk {
        background-color: #89b4fa;
        border-radius: 0px;
    }
    """)

    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)
