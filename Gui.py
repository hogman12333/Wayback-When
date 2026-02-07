import sys
import threading

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QLabel,
    QCheckBox, QSpinBox, QGroupBox, QScrollArea
)

from WaybackWhen import SETTINGS, normalize_url, CrawlCoordinator


class CrawlerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.coordinator = None
        self.worker_thread = None
        self.timer = None

        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("Wayback When")
        self.resize(1100, 700)

        root = QHBoxLayout(self)

        sidebar = QVBoxLayout()
        root.addLayout(sidebar, 1)

        url_row = QHBoxLayout()
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter URL")
        url_row.addWidget(self.url_entry)

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start)
        url_row.addWidget(self.start_btn)

        sidebar.addLayout(url_row)

        controls = QHBoxLayout()
        self.pause_btn = QPushButton("Pause")
        self.resume_btn = QPushButton("Resume")
        self.stop_btn = QPushButton("Stop")

        self.pause_btn.clicked.connect(self.pause)
        self.resume_btn.clicked.connect(self.resume)
        self.stop_btn.clicked.connect(self.stop)

        controls.addWidget(self.pause_btn)
        controls.addWidget(self.resume_btn)
        controls.addWidget(self.stop_btn)
        sidebar.addLayout(controls)

        sidebar.addWidget(QLabel("Settings"))

        settings_scroll = QScrollArea()
        settings_scroll.setWidgetResizable(True)
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)

        self.setting_widgets = {}

        for key, value in SETTINGS.items():
            box = QHBoxLayout()
            label = QLabel(key)
            box.addWidget(label)

            if isinstance(value, bool):
                w = QCheckBox()
                w.setChecked(value)
                w.stateChanged.connect(
                    lambda v, k=key: SETTINGS.__setitem__(k, bool(v))
                )

            elif isinstance(value, int):
                w = QSpinBox()
                w.setMaximum(10_000)
                w.setValue(value)
                w.valueChanged.connect(
                    lambda v, k=key: SETTINGS.__setitem__(k, v)
                )

            else:
                continue 

            box.addWidget(w)
            settings_layout.addLayout(box)
            self.setting_widgets[key] = w

        settings_layout.addStretch()
        settings_scroll.setWidget(settings_widget)
        sidebar.addWidget(settings_scroll)

        self.stats = QLabel("Archived: 0 | Skipped: 0 | Failed: 0 | Total: 0")
        sidebar.addWidget(self.stats)
        panel = QVBoxLayout()
        root.addLayout(panel, 3)

        panel.addWidget(QLabel("Crawl Queue"))
        self.crawl_list = QListWidget()
        panel.addWidget(self.crawl_list)

        panel.addWidget(QLabel("Archive Queue"))
        self.archive_list = QListWidget()
        panel.addWidget(self.archive_list)


    def start(self):
        url = self.url_entry.text().strip()
        if not url:
            return
        if "://" not in url:
            url = "http://" + url
        url = normalize_url(url)

        if self.worker_thread and self.worker_thread.is_alive():
            self.coordinator.add_url_live(url)
            return

        self.coordinator = CrawlCoordinator()
        self.coordinator.add_initial_urls([url])

        self.worker_thread = threading.Thread(
            target=self.coordinator.run, daemon=True
        )
        self.worker_thread.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.poll_state)
        self.timer.start(200)


    def pause(self):
        if self.coordinator:
            self.coordinator.pause()


    def resume(self):
        if self.coordinator:
            self.coordinator.resume()


    def stop(self):
        if self.coordinator:
            self.coordinator.stop()
        if self.timer:
            self.timer.stop()


    def poll_state(self):
        self.crawl_list.clear()
        self.crawl_list.addItems(
            [u[0] for u in self.coordinator.crawling_queue]
        )

        self.archive_list.clear()
        self.archive_list.addItems(
            list(self.coordinator.queue_for_archiving)
        )

        self.stats.setText(
            f"Archived: {self.coordinator.archived_count} | "
            f"Skipped: {self.coordinator.skipped_count} | "
            f"Failed: {self.coordinator.failed_count} | "
            f"Total: {self.coordinator.total_links_to_archive}"
        )


def main():
    app = QApplication(sys.argv)
    gui = CrawlerGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
