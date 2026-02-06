import sys
import threading
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFormLayout, QCheckBox, QSpinBox, QDoubleSpinBox,
    QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QObject

# Import your script
from WaybackWhen import SETTINGS, CrawlCoordinator


# -----------------------------
# Log signal bridge
# -----------------------------
class LogEmitter(QObject):
    log_signal = Signal(str)

log_emitter = LogEmitter()


# Patch your log_message to send logs to GUI
def gui_log_message(level, message, debug_only=False):
    if debug_only and not SETTINGS["debug_mode"]:
        return
    log_emitter.log_signal.emit(f"[{level.upper()}] {message}")

# Replace original logger
import main
main.log_message = gui_log_message


# -----------------------------
# GUI Window
# -----------------------------
class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Crawler & Archiver – GUI")
        self.setMinimumSize(700, 600)

        layout = QVBoxLayout(self)

        # URL input
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Target URLs (comma separated):"))
        self.url_input = QLineEdit()
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # Scrollable settings panel
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        settings_widget = QWidget()
        self.form = QFormLayout(settings_widget)

        self.widgets = {}
        self.build_settings_form()

        scroll.setWidget(settings_widget)
        layout.addWidget(scroll)

        # Start button
        self.start_button = QPushButton("Start Crawl")
        self.start_button.clicked.connect(self.start_crawl)
        layout.addWidget(self.start_button)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        # Connect log signal
        log_emitter.log_signal.connect(self.append_log)

    # -----------------------------
    # Build settings form dynamically
    # -----------------------------
    def build_settings_form(self):
        for key, value in SETTINGS.items():
            if isinstance(value, bool):
                widget = QCheckBox()
                widget.setChecked(value)
            elif isinstance(value, int):
                widget = QSpinBox()
                widget.setMaximum(999999)
                widget.setValue(value)
            elif isinstance(value, float):
                widget = QDoubleSpinBox()
                widget.setDecimals(3)
                widget.setMaximum(999999.0)
                widget.setValue(value)
            elif isinstance(value, list):
                widget = QLineEdit(", ".join(value))
            else:
                widget = QLineEdit(str(value))

            self.widgets[key] = widget
            self.form.addRow(QLabel(key), widget)

    # -----------------------------
    # Apply GUI settings → script SETTINGS
    # -----------------------------
    def apply_settings(self):
        for key, widget in self.widgets.items():
            if isinstance(widget, QCheckBox):
                SETTINGS[key] = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                SETTINGS[key] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                SETTINGS[key] = widget.value()
            else:
                text = widget.text().strip()
                if key == "proxies":
                    SETTINGS[key] = [p.strip() for p in text.split(",") if p.strip()]
                else:
                    SETTINGS[key] = text

    # -----------------------------
    # Start crawl in background thread
    # -----------------------------
    def start_crawl(self):
        urls = self.url_input.text().strip()
        if not urls:
            QMessageBox.warning(self, "Error", "Please enter at least one URL.")
            return

        self.apply_settings()

        url_list = [u.strip() for u in urls.split(",") if u.strip()]

        self.start_button.setEnabled(False)
        self.log_output.append("Starting crawl...\n")

        thread = threading.Thread(target=self.run_crawl, args=(url_list,), daemon=True)
        thread.start()

    def run_crawl(self, urls):
        try:
            coordinator = CrawlCoordinator()
            coordinator.add_initial_urls(urls)
            coordinator.run()
        except Exception as e:
            log_emitter.log_signal.emit(f"[ERROR] {e}")
        finally:
            log_emitter.log_signal.emit("Crawl finished.\n")
            self.start_button.setEnabled(True)

    # -----------------------------
    # Log output
    # -----------------------------
    def append_log(self, text):
        self.log_output.append(text)


# -----------------------------
# Main entry
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())
