from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(35, 35, 35))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 204))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(127, 127, 127))

    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #e0e0e0;
        background-color: #1e1e1e;
    }

    QGroupBox { 
        border: 2px solid #141414;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #1e1e1e;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #D8D8D8;
        font-weight: bold;
    }

    QListWidget, QTextEdit, QLineEdit {
        background-color: #2d2d30;
        color: #e0e0e0;
        border: 1px solid #404040;
        border-radius: 4px;
        padding: 0px;
        selection-background-color: #5F5F5F;
        selection-color: white;
    }

    QPushButton {
        background-color: #333337;
        color: #e0e0e0;
        border: 1px solid #404040;
        border-radius: 4px;
        padding: 8px 12px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #3a3a3d;
        border-color: #00ccff;
    }

    QPushButton:pressed {
        background-color: #1e1e1e;
    }

    QPushButton:disabled {
        color: #777;
        background-color: #2d2d30;
    }

    QMenuBar {
        background-color: #252526;
        color: #e0e0e0;
        border-bottom: 1px solid #404040;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
    }

    QMenuBar::item:selected {
        background-color: #3e3e40;
    }

    QMenu {
        background-color: #2d2d30;
        color: #e0e0e0;
        border: 1px solid #404040;
    }

    QMenu::item:selected {
        background-color: #3e3e40;
    }

    QScrollBar:vertical {
        border: 1px solid #573D3D;
        background: #2d2d30;
        width: 15px;
        margin: 0;
    }

    QScrollBar:horizontal {
        border: 1px solid #404040;
        background: #2d2d30;
        height: 15px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: #3e3e40;
        min-height: 20px;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background: #3e3e40;
        min-width: 20px;
        border-radius: 7px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }

    QProgressBar {
        border: 1px solid #404040;
        border-radius: 4px;
        text-align: center;
        background-color: #2d2d30;
    }

    QProgressBar::chunk {
        border-radius: 0px;
    }
    """)
