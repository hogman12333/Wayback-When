import sys
import time
from urllib.parse import urlparse

from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QLabel,
    QCheckBox, QSpinBox, QGroupBox, QTextEdit
)
from WaybackWhen import SETTINGS, normalize_url, get_root_domain, Coordinator

class QtStream(QObject):
    message = pyqtSignal(str)

    def write(self, text: str):
        text = text.rstrip("\n")
        if text:
            self.message.emit(text)

    def flush(self):
        pass
class CrawlerWorker(QObject):
    crawlQueueUpdated = pyqtSignal(list)
    archiveQueueUpdated = pyqtSignal(list)
    statsUpdated = pyqtSignal(dict)
    logMessage = pyqtSignal(str)

    def __init__(self, coordinator: Coordinator):
        super().__init__()
        self.coordinator = coordinator
        self.running = True

    def run(self):
        self.logMessage.emit("Crawler worker started.")
        while self.running:
            try:
                self.coordinator.step()
                self.emit_state()
                time.sleep(0.01)
            except Exception as e:
                self.logMessage.emit(f"Worker error: {e}")

        self.logMessage.emit("Crawler worker stopped.")

    def emit_state(self):
        crawl_items = [str(item) for item in self.coordinator.crawling_queue]
        archive_items = [str(item) for item in self.coordinator.queue_for_archiving]

        self.crawlQueueUpdated.emit(crawl_items)
        self.archiveQueueUpdated.emit(archive_items)
        self.statsUpdated.emit(self.coordinator.get_stats())

    def stop(self):
        self.running = False
        self.logMessage.emit("Crawler worker stopping.")
class CrawlerGUI(QWidget):
    def __init__(self, coordinator: Coordinator):
        super().__init__()
        self.coordinator = coordinator
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Wayback When")
        self.resize(1000, 650)
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(5, 5, 5, 5)
        sidebar.setSpacing(10)

        panel = QVBoxLayout()
        panel.setContentsMargins(5, 5, 5, 5)
        panel.setSpacing(10)

        main_layout.addLayout(sidebar, 1)   
        main_layout.addLayout(panel, 3)     

        url_row = QHBoxLayout()
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter URL to add...")
        add_btn = QPushButton("Add URL")
        add_btn.clicked.connect(self.add_url)
        url_row.addWidget(self.url_entry)
        url_row.addWidget(add_btn)
        sidebar.addLayout(url_row)

        settings_box = QGroupBox("Settings")
        settings_layout = QVBoxLayout()

        self.debug_checkbox = QCheckBox("Debug Mode")
        self.debug_checkbox.setChecked(SETTINGS.get("debug_mode", False))
        self.debug_checkbox.stateChanged.connect(self.toggle_debug)
        settings_layout.addWidget(self.debug_checkbox)

        settings_layout.addWidget(QLabel("Crawler Workers"))
        self.worker_spin = QSpinBox()
        self.worker_spin.setMinimum(0)
        self.worker_spin.setMaximum(100)
        self.worker_spin.setValue(SETTINGS.get("max_crawler_workers", 0))
        self.worker_spin.valueChanged.connect(self.update_workers)
        settings_layout.addWidget(self.worker_spin)

        settings_box.setLayout(settings_layout)
        sidebar.addWidget(settings_box)
        
        self.stats_label = QLabel("Archived: 0 | Skipped: 0 | Failed: 0 | Total: 0")
        sidebar.addWidget(self.stats_label)


        sidebar.addStretch(1)

        panel.addWidget(QLabel("Crawl Queue"))
        self.crawl_list = QListWidget()
        panel.addWidget(self.crawl_list)

        panel.addWidget(QLabel("Archive Queue"))
        self.archive_list = QListWidget()
        panel.addWidget(self.archive_list)

        panel.addWidget(QLabel("Log"))
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        panel.addWidget(self.log_view)

    def add_url(self):
        url = self.url_entry.text().strip()
        if not url:
            return

        if "://" not in url:
            url = "http://" + url
        try:
            normalized = normalize_url(url)
        except Exception:
            normalized = url

        self.coordinator.add_url_live(normalized)
        print(f"[GUI] Added URL: {normalized}")
        self.url_entry.clear()

    def toggle_debug(self, state):
        SETTINGS["debug_mode"] = bool(state)
        print(f"[GUI] Debug mode set to: {SETTINGS['debug_mode']}")

    def update_workers(self, value):
        SETTINGS["max_crawler_workers"] = value
        print(f"[GUI] Max crawler workers set to: {value}")


    def update_crawl_queue(self, items):
        self.crawl_list.clear()
        self.crawl_list.addItems(items)

    def update_archive_queue(self, items):
        self.archive_list.clear()
        self.archive_list.addItems(items)

    def update_stats(self, stats):
        archived = stats.get("archived", 0)
        skipped = stats.get("skipped", 0)
        failed = stats.get("failed", 0)
        total = stats.get("total", 0)
        self.stats_label.setText(
            f"Archived: {archived} | "
            f"Skipped: {skipped} | "
            f"Failed: {failed} | "
            f"Total: {total}"
        )

    def append_log(self, msg: str):
        self.log_view.append(msg)


def main():
    app = QApplication(sys.argv)

    coordinator = Coordinator()
    gui = CrawlerGUI(coordinator)

    qt_stream = QtStream()
    qt_stream.message.connect(gui.append_log)
    sys.stdout = qt_stream
    sys.stderr = qt_stream

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
