from PyQt6.QtWidgets import QApplication


def apply(app, widget):
    app.setPalette(QApplication.style().standardPalette())

    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #313030;
    }

    QGroupBox {
        border: 2px solid #c0c0c0;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #fafafa;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #1E1F20;
        font-weight: bold;
    }

    QListWidget, QTextEdit, QLineEdit {
        border: 1px solid #c0c0c0;
        border-radius: 4px;
        padding: 6px;
        background-color: white;
        color: #242424;
        selection-background-color: #777777;
        selection-color: white;
    }

    QPushButton {
        padding: 8px 12px;
        border-radius: 4px;
        border: 1px solid #c0c0c0;
        background-color: #f0f0f0;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #e0e0e0;
        border-color: #A1A1A1;
    }

    QPushButton:pressed {
        background-color: #d0d0d0;
    }

    QPushButton:disabled {
        color: #a0a0a0;
        background-color: #f8f8f8;
    }

    QMenuBar {
        background-color: #f0f0f0;
        border-bottom: 1px solid #c0c0c0;
    }

    QMenuBar::item:selected {
        background-color: #e0e0e0;
    }

    QScrollBar:vertical,
    QScrollBar:horizontal {
        border: 1px solid #c0c0c0;
        background: #f0f0f0;
        margin: 0;
    }

    QScrollBar:vertical {
        width: 15px;
    }

    QScrollBar:horizontal {
        height: 15px;
    }

    QScrollBar::handle:vertical,
    QScrollBar::handle:horizontal {
        background: #c0c0c0;
        border-radius: 7px;
        min-height: 20px;
        min-width: 20px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }

    QProgressBar {
        border: 1px solid #c0c0c0;
        border-radius: 4px;
        text-align: center;
        background-color: #f0f0f0;
    }

    QProgressBar::chunk {
        background-color: #0078d4;
    }
    """)
