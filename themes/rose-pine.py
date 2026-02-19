from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(31, 29, 46))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(224, 222, 244))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 23, 36))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(38, 35, 58))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(224, 222, 244))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(224, 222, 244))
    palette.setColor(QPalette.ColorRole.Text, QColor(224, 222, 244))
    palette.setColor(QPalette.ColorRole.Button, QColor(64, 61, 82))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(224, 222, 244))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(235, 111, 146))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(49, 116, 143))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(224, 222, 244))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(144, 140, 170))

    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #e0def4;
        background-color: #1f1d2e;
    }

    QGroupBox { 
        border: 2px solid #26233a;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #1f1d2e;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #e0def4;
        font-weight: bold;
    }

    QListWidget, QTextEdit, QLineEdit {
        background-color: #26233a;
        color: #e0def4;
        border: 1px solid #403d52;
        border-radius: 4px;
        padding: 0px;
        selection-background-color: #31748f;
        selection-color: #e0def4;
    }

    QPushButton {
        background-color: #26233a;
        color: #e0def4;
        border: 1px solid #403d52;
        border-radius: 4px;
        padding: 8px 12px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #403d52;
        border-color: #c4a7e7;
    }

    QPushButton:pressed {
        background-color: #191724;
    }

    QPushButton:disabled {
        color: #6e6a86;
        background-color: #26233a;
    }

    QMenuBar {
        background-color: #191724;
        color: #e0def4;
        border-bottom: 1px solid #403d52;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
    }

    QMenuBar::item:selected {
        background-color: #44415a;
    }

    QMenu {
        background-color: #26233a;
        color: #e0def4;
        border: 1px solid #403d52;
    }

    QMenu::item:selected {
        background-color: #44415a;
    }

    QScrollBar:vertical {
        border: 1px solid #403d52;
        background: #26233a;
        width: 15px;
        margin: 0;
    }

    QScrollBar:horizontal {
        border: 1px solid #403d52;
        background: #26233a;
        height: 15px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: #44415a;
        min-height: 20px;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background: #44415a;
        min-width: 20px;
        border-radius: 7px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }

    QProgressBar {
        border: 1px solid #403d52;
        border-radius: 4px;
        text-align: center;
        background-color: #26233a;
    }

    QProgressBar::chunk {
        border-radius: 0px;
        background-color: #433D68;
    }
    """)

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)
