from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(40, 40, 45, 220)) 
    palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240, 240))
    palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 40, 200)) 
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(40, 40, 45, 200))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(50, 50, 55, 240))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(240, 240, 240, 240))
    palette.setColor(QPalette.ColorRole.Text, QColor(240, 240, 240, 240))
    palette.setColor(QPalette.ColorRole.Button, QColor(55, 55, 60, 200))  
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 240, 240, 240))  
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 150, 150, 240))  
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 204, 200))  
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(180, 180, 180, 200)) 

    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: rgba(240, 240, 240, 240);
        background-color: rgba(30, 30, 35, 160);
    }
    
    QMainWindow, QDialog {
        background-color: rgba(30, 30, 35, 180);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
    }

    QGroupBox { 
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: rgba(50, 50, 55, 200);
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0px 10px 0px 10px;
        color: rgba(240, 240, 240, 240);
        font-weight: bold;
        font-size: 11pt;
    }

    QListWidget, QTextEdit, QLineEdit {
        background-color: rgba(60, 60, 65, 220);
        color: rgba(240, 240, 240, 240);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        padding: 5px 8px;
        selection-background-color: rgba(0, 122, 204, 200);
        selection-color: white;
    }

    QLineEdit:focus {
        border: 1px solid rgba(0, 180, 255, 0.5);
    }

    QPushButton {
        background-color: rgba(65, 65, 70, 220);
        color: rgba(240, 240, 240, 240);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
    }

    QPushButton:hover {
        background-color: rgba(85, 85, 90, 240);
        border-color: rgba(0, 180, 255, 0.5);
    }

    QPushButton:pressed {
        background-color: rgba(65, 65, 70, 240);
        border-color: rgba(0, 180, 255, 0.6);
    }

    QPushButton:disabled {
        color: rgba(200, 200, 200, 180);
        background-color: rgba(65, 65, 70, 160);
    }

    QMenuBar {
        background-color: rgba(50, 50, 55, 200);
        color: rgba(240, 240, 240, 240);
        border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 5px 12px;
        border-radius: 4px;
    }

    QMenuBar::item:selected {
        background-color: rgba(85, 85, 90, 220);
    }

    QMenu {
        background-color: rgba(55, 55, 60, 240);
        color: rgba(240, 240, 240, 240);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 8px 0px;
    }

    QMenu::item {
        padding: 6px 24px 6px 16px;
        margin: 2px 8px;
        border-radius: 4px;
    }

    QMenu::item:selected {
        background-color: rgba(85, 85, 90, 200);
    }

    QMenu::separator {
        height: 1px;
        background: rgba(255, 255, 255, 0.15);
        margin: 6px 8px;
    }

    QScrollBar:vertical {
        border: none;
        background: rgba(50, 50, 55, 160);
        width: 12px;
        margin: 2px;
    }

    QScrollBar:horizontal {
        border: none;
        background: rgba(50, 50, 55, 160);
        height: 12px;
        margin: 2px;
    }

    QScrollBar::handle:vertical {
        background: rgba(200, 200, 200, 150);
        min-height: 20px;
        border-radius: 6px;
    }

    QScrollBar::handle:horizontal {
        background: rgba(200, 200, 200, 150);
        min-width: 20px;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical:hover {
        background: rgba(220, 220, 220, 180);
    }

    QScrollBar::handle:horizontal:hover {
        background: rgba(220, 220, 220, 180);
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0px;
        width: 0px;
    }

    QScrollBar::add-page, QScrollBar::sub-page {
        background: transparent;
    }

    QProgressBar {
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        text-align: center;
        background-color: rgba(60, 60, 65, 200);
        padding: 1px;
    }

    QProgressBar::chunk {
        border-radius: 7px;
        background-color: rgba(0, 150, 255, 220);
    }

    QToolTip {
        background-color: rgba(55, 55, 60, 240);
        color: rgba(240, 240, 240, 240);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 6px;
        padding: 4px 8px;
    }
    """)

    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
    if widget.inherits("QMainWindow") or widget.inherits("QDialog"):
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(8)  
        widget.setGraphicsEffect(blur)
        
        class FrostedBackground(QWidget):
            def paintEvent(self, event):
                painter = QPainter(self)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                path = QPainterPath()
                path.addRoundedRect(self.rect(), 12, 12)
                painter.setClipPath(path)
                painter.fillRect(self.rect(), QColor(40, 40, 45, 220))  
                painter.setPen(QColor(255, 255, 255, 50)) 
                painter.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 11, 11)
        
        bg = FrostedBackground(widget)
        bg.setGeometry(widget.rect())
        widget.resizeEvent = lambda e: bg.setGeometry(widget.rect())
        bg.lower()
