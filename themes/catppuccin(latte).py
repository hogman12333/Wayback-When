from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
def apply(app, widget):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(239, 241, 245))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(76, 79, 105))
    palette.setColor(QPalette.ColorRole.Base, QColor(239, 241, 245))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(230, 233, 239))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(230, 233, 239))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(76, 79, 105))
    palette.setColor(QPalette.ColorRole.Text, QColor(76, 79, 105))
    palette.setColor(QPalette.ColorRole.Button, QColor(220, 224, 232))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(76, 79, 105))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(64, 160, 43))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(30, 102, 245))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(230, 233, 239))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(152, 157, 180))
    app.setPalette(palette)
    widget.setStyleSheet("""
    QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 11pt;
    color: #4c4f69;
    background-color: #eff1f5;
    }
    QGroupBox {
    border: 2px solid #dce0e8;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: #e6e9ef;
    }
    QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #5c5f77;
    font-weight: bold;
    }
    QListWidget, QTextEdit, QLineEdit {
    background-color: #ffffff;
    color: #4c4f69;
    border: 1px solid #9ca0b0;
    border-radius: 4px;
    padding: 0px;
    selection-background-color: #dfe1e8;
    selection-color: #4c4f69;
    }
    QPushButton {
    background-color: #e6e9ef;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 4px;
    padding: 8px 12px;
    font-weight: bold;
    }
    QPushButton:hover {
    background-color: #dfe1e8;
    border-color: #1e66f5;
    }
    QPushButton:pressed {
    background-color: #dce0e8;
    }
    QPushButton:disabled {
    color: #9ca0b0;
    background-color: #eff1f5;
    }
    QMenuBar {
    background-color: #e6e9ef;
    color: #4c4f69;
            border
    -bottom: 1px solid #dce0e8;
    }
    QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
    }
    QMenuBar::item:selected {
    background-color: #dfe1e8;
    }

        QMenu {
    background-color: #ffffff;
    color: #4c4f69;
    border: 1px solid #dce0e8;
    }
    QMenu::item:selected {
    background-color: #dfe1e8;
    }
    QScrollBar:vertical {
    border: 1px solid #dce0e8;
    background: #e6e9ef;
    width: 15px;
    margin: 0;
    }
    QScrollBar:horizontal {
    border: 1px solid #dce0e8;
    background: #e6e9ef;
    height: 15px;
    margin: 0;
    }
    QScrollBar::handle:vertical {
    background: #acb0be;
    min-height: 20px;
    border-radius: 7px;
    }
    QScrollBar::handle:horizontal {
    background: #acb0be;
    min-width: 20px;
    border-radius: 7px;
    }
    QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
    }
    QProgressBar {
    border: 1px solid #dce0e8;
    border-radius: 4px;
    text-align: center;
    background-color: #e6e9ef;
    }
    QProgressBar::chunk {
            background-color
    : #1e66f5;
            border
    -radius: 0px;
    }
    """)
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)
