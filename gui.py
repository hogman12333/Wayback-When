# crawler_gui.py

import sys
from urllib.parse import urlparse

from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QLabel,
    QCheckBox, QSpinBox, QGroupBox, QTextEdit
)

# Import your crawler logic
from WaybackWhen import SETTINGS, normalize_url, get_root_domain, Coordinator


# ---------------- Worker Thread ---------------- #

class CrawlerWorker(QObject):
    crawlQueueUpdated = pyqtSignal(list)
    archiveQueueUpdated = pyqtSignal(list)
    statsUpdated = pyqtSignal(dict)
    logMessage = pyqtSignal(str)

    def __init__(self, coordinator):
        super().__init__()
        self.coordinator = coordinator
        self.running = True

    def run(self):
        self.logMessage.emit("Crawler worker started.")
        while self.running:
            try:
                self.coordinator.step()
                self.emit_state()
            except Exception as e:
                self.logMessage.emit(f"Worker error: {e}")

    def emit_state(self):
        self.crawlQueueUpdated.emit(list(self.coordinator.crawling_queue))
        self.archiveQueueUpdated.emit(list(self.coordinator.queue_for_archiving))
        self.statsUpdated.emit(self.coordinator.get_stats())

    def stop(self):
        self.running = False
        self.logMessage.emit("Crawler worker stopping.")


# ---------------- GUI ---------------- #

class CrawlerGUI(QWidget):
    def __init__(self, coordinator):
        super().__init__()
        self.coordinator = coordinator
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Crawler Control Panel")
        self.resize(900, 600)

        layout = QVBoxLayout()

        # URL input
        url_row = QHBoxLayout()
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter URL to add...")
        add_btn = QPushButton("Add URL")
        add_btn.clicked.connect(self.add_url)
        url_row.addWidget(self.url_entry)
        url_row.addWidget(add_btn)
        layout.addLayout(url_row)

        # Crawl queue
        layout.addWidget(QLabel("Crawl Queue"))
        self.crawl_list = QListWidget()
        layout.addWidget(self.crawl_list)

        # Archive queue
        layout.addWidget(QLabel("Archive Queue"))
        self.archive_list = QListWidget()
        layout.addWidget(self.archive_list)

        # Stats
        self.stats_label = QLabel("Stats will appear here")
        layout.addWidget(self.stats_label)

        # Settings
        settings_box = QGroupBox("Settings")
        settings_layout = QVBoxLayout()

        self.debug_checkbox = QCheckBox("Debug Mode")
        self.debug_checkbox.setChecked(SETTINGS["debug_mode"])
        self.debug_checkbox.stateChanged.connect(self.toggle_debug)
        settings_layout.addWidget(self.debug_checkbox)

        self.worker_spin = QSpinBox()
        self.worker_spin.setMinimum(0)
        self.worker_spin.setMaximum(100)
        self.worker_spin.setValue(SETTINGS["max_crawler_workers"])
        self.worker_spin.valueChanged.connect(self.update_workers)
        settings_layout.addWidget(QLabel("Crawler Workers"))
        settings_layout.addWidget(self.worker_spin)

        settings_box.setLayout(settings_layout)
        layout.addWidget(settings_box)

        # Log panel
        layout.addWidget(QLabel("Log"))
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view)

        self.setLayout(layout)

    # ---- GUI Actions ---- #

    def add_url(self):
        url = self.url_entry.text().strip()
        if url:
            self.coordinator.add_url_live(url)
            self.url_entry.clear()

    def toggle_debug(self, state):
        SETTINGS["debug_mode"] = bool(state)

    def update_workers(self, value):
        SETTINGS["max_crawler_workers"] = value

    # ---- Worker Signal Slots ---- #

    def update_crawl_queue(self, items):
        self.crawl_list.clear()
        self.crawl_list.addItems(items)

    def update_archive_queue(self, items):
        self.archive_list.clear()
        self.archive_list.addItems(items)

    def update_stats(self, stats):
        self.stats_label.setText(
            f"Archived: {stats['archived']} | "
            f"Skipped: {stats['skipped']} | "
            f"Failed: {stats['failed']} | "
            f"Total: {stats['total']}"
        )

    def append_log(self, msg):
        self.log_view.append(msg)


# ---------------- Entrypoint ---------------- #

def main():
    app = QApplication(sys.argv)

    coordinator = Coordinator()

    gui = CrawlerGUI(coordinator)

    thread = QThread()
    worker = CrawlerWorker(coordinator)
    worker.moveToThread(thread)

    thread.started.connect(worker.run)

    worker.crawlQueueUpdated.connect(gui.update_crawl_queue)
    worker.archiveQueueUpdated.connect(gui.update_archive_queue)
    worker.statsUpdated.connect(gui.update_stats)
    worker.logMessage.connect(gui.append_log)

    def shutdown():
        worker.stop()
        thread.quit()
        thread.wait()

    app.aboutToQuit.connect(shutdown)

    thread.start()
    gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
