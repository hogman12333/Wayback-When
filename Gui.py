import sys
import threading
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QLabel,
    QCheckBox, QSpinBox, QGroupBox
)

from WaybackWhen import SETTINGS, normalize_url, CrawlCoordinator


class CoordinatorWorker(QObject):
    statsUpdated = pyqtSignal(dict)
    queuesUpdated = pyqtSignal(list, list)

    def __init__(self, coordinator: CrawlCoordinator):
        super().__init__()
        self.coordinator = coordinator

    def run(self):
        self.coordinator.run()
        self.emit_state()

    def emit_state(self):
        self.statsUpdated.emit({
            "archived": self.coordinator.archived_count,
            "skipped": self.coordinator.skipped_count,
            "failed": self.coordinator.failed_count,
            "total": self.coordinator.total_links_to_archive,
        })
        self.queuesUpdated.emit(
            [u[0] for u in self.coordinator.crawling_queue],
            list(self.coordinator.queue_for_archiving),
        )


class CrawlerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.coordinator = CrawlCoordinator()
        self.worker = CoordinatorWorker(self.coordinator)
        self.worker_thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Wayback When")
        self.resize(900, 600)

        layout = QHBoxLayout(self)

        left = QVBoxLayout()
        right = QVBoxLayout()
        layout.addLayout(left, 1)
        layout.addLayout(right, 3)

        row = QHBoxLayout()
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter URL…")
        add_btn = QPushButton("Start Crawl")
        add_btn.clicked.connect(self.start_crawl)
        row.addWidget(self.url_entry)
        row.addWidget(add_btn)
        left.addLayout(row)

        box = QGroupBox("Settings")
        box_l = QVBoxLayout(box)

        self.debug_cb = QCheckBox("Debug mode")
        self.debug_cb.setChecked(SETTINGS["debug_mode"])
        self.debug_cb.stateChanged.connect(
            lambda v: SETTINGS.__setitem__("debug_mode", bool(v))
        )
        box_l.addWidget(self.debug_cb)

        box_l.addWidget(QLabel("Crawler workers"))
        spin = QSpinBox()
        spin.setRange(0, 100)
        spin.setValue(SETTINGS["max_crawler_workers"])
        spin.valueChanged.connect(
            lambda v: SETTINGS.__setitem__("max_crawler_workers", v)
        )
        box_l.addWidget(spin)

        left.addWidget(box)

        self.stats = QLabel("Archived: 0 | Skipped: 0 | Failed: 0 | Total: 0")
        left.addWidget(self.stats)
        left.addStretch()

        # Queues
        right.addWidget(QLabel("Crawl Queue"))
        self.crawl_list = QListWidget()
        right.addWidget(self.crawl_list)

        right.addWidget(QLabel("Archive Queue"))
        self.archive_list = QListWidget()
        right.addWidget(self.archive_list)

        self.worker.statsUpdated.connect(self.update_stats)
        self.worker.queuesUpdated.connect(self.update_queues)

    def start_crawl(self):
        url = self.url_entry.text().strip()
        if not url:
            return
        if "://" not in url:
            url = "http://" + url

        url = normalize_url(url)
        self.coordinator.add_initial_urls([url])

        self.worker_thread = threading.Thread(target=self.worker.run, daemon=True)
        self.worker_thread.start()

    def update_stats(self, s):
        self.stats.setText(
            f"Archived: {s['archived']} | "
            f"Skipped: {s['skipped']} | "
            f"Failed: {s['failed']} | "
            f"Total: {s['total']}"
        )

    def update_queues(self, crawl, archive):
        self.crawl_list.clear()
        self.crawl_list.addItems(crawl)
        self.archive_list.clear()
        self.archive_list.addItems(archive)


def main():
    app = QApplication(sys.argv)
    gui = CrawlerGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
