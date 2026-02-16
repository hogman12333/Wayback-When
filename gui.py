import sys
import threading

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QLabel,
    QCheckBox, QSpinBox, QGroupBox, QScrollArea, QTextEdit
)

from urllib.parse import urlparse

from WaybackWhen import SETTINGS, normalize_url, CrawlCoordinator, log_message, get_root_domain

class CrawlerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.coordinator = None
        self.worker_thread = None
        self.timer = None
        self.is_running = False
        self.is_paused = False

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Wayback When")
        self.resize(1100, 700)

        root = QHBoxLayout(self)

        sidebar = QVBoxLayout()
        root.addLayout(sidebar, 1)

        url_group = QGroupBox("URL Management")
        url_layout = QVBoxLayout()

        url_row = QHBoxLayout()
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter URL")
        url_row.addWidget(self.url_entry, 4)
        
        self.add_url_btn = QPushButton("Add URL")
        self.add_url_btn.clicked.connect(self.add_url)
        url_row.addWidget(self.add_url_btn, 1)
        
        url_layout.addLayout(url_row)
        self.url_list = QListWidget()
        url_layout.addWidget(self.url_list)
        
        control_btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_crawling)
        control_btn_layout.addWidget(self.start_btn)
        
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.pause)
        self.pause_btn.setEnabled(False)
        control_btn_layout.addWidget(self.pause_btn)
        
        self.resume_btn = QPushButton("Resume")
        self.resume_btn.clicked.connect(self.resume)
        self.resume_btn.setEnabled(False)
        control_btn_layout.addWidget(self.resume_btn)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        control_btn_layout.addWidget(self.stop_btn)
        
        url_layout.addLayout(control_btn_layout)
        url_group.setLayout(url_layout)
        sidebar.addWidget(url_group)

        proxy_group = QGroupBox("Proxy Configuration")
        proxy_layout = QVBoxLayout()
        
        proxy_label = QLabel("Proxies (one per line, format: http://user:pass@host:port):")
        proxy_layout.addWidget(proxy_label)
        
        self.proxy_text = QTextEdit()
        self.proxy_text.setMaximumHeight(100)
        self.proxy_text.setPlaceholderText("http://user:pass@host:port\nhttp://anotherproxy:8080")
        proxy_layout.addWidget(self.proxy_text)
        
        proxy_btn_layout = QHBoxLayout()
        self.save_proxy_btn = QPushButton("Save Proxies")
        self.save_proxy_btn.clicked.connect(self.save_proxies)
        proxy_btn_layout.addWidget(self.save_proxy_btn)
        
        self.clear_proxy_btn = QPushButton("Clear Proxies")
        self.clear_proxy_btn.clicked.connect(self.clear_proxies)
        proxy_btn_layout.addWidget(self.clear_proxy_btn)
        
        proxy_layout.addLayout(proxy_btn_layout)
        proxy_group.setLayout(proxy_layout)
        sidebar.addWidget(proxy_group)

        settings_group = QGroupBox("Settings")
        sidebar.addWidget(settings_group)
        settings_layout = QVBoxLayout(settings_group)

        settings_scroll = QScrollArea()
        settings_scroll.setWidgetResizable(True)
        settings_widget = QWidget()
        settings_inner_layout = QVBoxLayout(settings_widget)

        self.setting_widgets = {}

        for key, value in SETTINGS.items():
            if key == "proxies":
                continue
                
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
            settings_inner_layout.addLayout(box)
            self.setting_widgets[key] = w

        settings_inner_layout.addStretch()
        settings_scroll.setWidget(settings_widget)
        settings_layout.addWidget(settings_scroll)
        self.stats = QLabel("Status: Ready | Archived: 0 | Skipped: 0 | Failed: 0 | Total: 0")
        sidebar.addWidget(self.stats)
        panel = QVBoxLayout()
        root.addLayout(panel, 3)
        panel.addWidget(QLabel("Crawl Queue"))
        self.crawl_list = QListWidget()
        panel.addWidget(self.crawl_list)
        panel.addWidget(QLabel("Archive Queue"))
        self.archive_list = QListWidget()
        panel.addWidget(self.archive_list)
        self.update_proxy_display()

    def add_url(self):
        """Add a URL to the list of URLs to process"""
        url = self.url_entry.text().strip()
        if not url:
            return
            
        if "://" not in url:
            url = "http://" + url
            
        self.url_list.addItem(url)
        self.url_entry.clear()
        
        if self.is_running and self.coordinator:
            try:
                self.coordinator.add_url_live(url)
                log_message("INFO", f"Added URL while running: {url}", debug_only=False)
            except Exception as e:
                log_message("ERROR", f"Failed to add URL: {str(e)}", debug_only=False)

    def save_proxies(self):
        """Parse and save proxy settings from the text box"""
        proxy_text = self.proxy_text.toPlainText().strip()
        if not proxy_text:
            SETTINGS["proxies"] = []
            log_message("INFO", "Proxy list cleared", debug_only=True)
            self.update_proxy_display()
            return

        proxies = []
        for line in proxy_text.split('\n'):
            proxy = line.strip()
            if proxy:
                try:
                    parsed = urlparse(proxy)
                    if not all([parsed.scheme, parsed.netloc]):
                        log_message("WARNING", f"Invalid proxy format: {proxy}", debug_only=True)
                        continue
                    proxies.append(proxy)
                except Exception as e:
                    log_message("ERROR", f"Error parsing proxy {proxy}: {e}", debug_only=True)

        SETTINGS["proxies"] = proxies
        log_message("INFO", f"Saved {len(proxies)} proxies", debug_only=True)
        self.update_proxy_display()

    def clear_proxies(self):
        """Clear the proxy list"""
        SETTINGS["proxies"] = []
        self.update_proxy_display()
        log_message("INFO", "Proxies cleared", debug_only=True)

    def update_proxy_display(self):
        """Update the proxy text box with current settings"""
        self.proxy_text.setPlainText("\n".join(SETTINGS.get("proxies", [])))

    def start_crawling(self):
        """Start the crawling process with all URLs in the list"""
        if self.url_list.count() == 0:
            log_message("WARNING", "No URLs to process", debug_only=False)
            return
            
        self.save_proxies()

        if self.worker_thread and self.worker_thread.is_alive():
            log_message("INFO", "Crawler is already running", debug_only=False)
            return
        urls = [self.url_list.item(i).text() for i in range(self.url_list.count())]
        
        self.coordinator = CrawlCoordinator()
        self.coordinator.add_initial_urls(urls)

        self.worker_thread = threading.Thread(
            target=self.coordinator.run, daemon=True
        )
        self.worker_thread.start()
        self.is_running = True
        self.update_button_states()

        self.timer = QTimer()
        self.timer.timeout.connect(self.poll_state)
        self.timer.start(200)

    def pause(self):
        if self.coordinator:
            self.coordinator.pause()
            self.is_paused = True
            self.update_button_states()

    def resume(self):
        if self.coordinator:
            self.coordinator.resume()
            self.is_paused = False
            self.update_button_states()

    def stop(self):
        if self.coordinator:
            self.coordinator.stop()
        if self.timer:
            self.timer.stop()
        self.is_running = False
        self.is_paused = False
        self.update_button_states()

    def poll_state(self):
        if not self.coordinator:
            return

        # Update crawl queue
        self.crawl_list.clear()
        if hasattr(self.coordinator, 'crawling_queue'):
            self.crawl_list.addItems(
                [u[0] for u in self.coordinator.crawling_queue]
            )

        # Update archive queue
        self.archive_list.clear()
        if hasattr(self.coordinator, 'queue_for_archiving'):
            self.archive_list.addItems(
                list(self.coordinator.queue_for_archiving)
            )
        if hasattr(self.coordinator, 'archived_count'):
            status = "Running"
            if self.is_paused:
                status = "Paused"
                
            self.stats.setText(
                f"Status: {status} | "
                f"Archived: {self.coordinator.archived_count} | "
                f"Skipped: {self.coordinator.skipped_count} | "
                f"Failed: {self.coordinator.failed_count} | "
                f"Total: {getattr(self.coordinator, 'total_links_to_archive', 0)}"
            )

    def update_button_states(self):
        """Update button states based on current crawler state"""
        self.start_btn.setEnabled(not self.is_running)
        self.add_url_btn.setEnabled(True)
        self.pause_btn.setEnabled(self.is_running and not self.is_paused)
        self.resume_btn.setEnabled(self.is_running and self.is_paused)
        self.stop_btn.setEnabled(self.is_running)


def main():
    app = QApplication(sys.argv)
    gui = CrawlerGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
