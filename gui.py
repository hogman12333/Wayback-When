import sys
import threading
import json
from pathlib import Path
from collections import deque

from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QObject
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QLabel,
    QCheckBox, QSpinBox, QGroupBox, QScrollArea, QTextEdit, 
    QStyleFactory, QDialog, QDialogButtonBox, QMenu, QMenuBar,
    QProgressBar, QFrame, QListWidgetItem
)
from PyQt6.QtGui import QPalette, QColor, QAction, QFont, QIcon

from urllib.parse import urlparse

from WaybackWhen import SETTINGS, normalize_url, CrawlCoordinator, log_message, get_root_domain

SETTINGS_FILE = "settings.txt"

def save_settings():
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(SETTINGS, f, indent=2)
        log_message("INFO", f"Settings saved to {SETTINGS_FILE}", debug_only=True)
    except Exception as e:
        log_message("ERROR", f"Failed to save settings: {str(e)}", debug_only=False)

def load_settings():
    try:
        if Path(SETTINGS_FILE).exists():
            with open(SETTINGS_FILE, 'r') as f:
                loaded = json.load(f)
                SETTINGS.update(loaded)
            log_message("INFO", f"Settings loaded from {SETTINGS_FILE}", debug_only=True)
        else:
            # Set default dark mode if no settings file exists
            SETTINGS["dark_mode"] = True
            save_settings()
    except Exception as e:
        log_message("ERROR", f"Failed to load settings: {str(e)}", debug_only=False)
        # Set default dark mode on error
        SETTINGS["dark_mode"] = True
        save_settings()

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setSpacing(10)
        
        self.setting_widgets = {}
        
        for key, value in SETTINGS.items():
            if key == "proxies":
                continue
                
            box = QHBoxLayout()
            label = QLabel(f"{key.replace('_', ' ').title()}:")
            box.addWidget(label, 1)

            if isinstance(value, bool):
                w = QCheckBox()
                w.setChecked(value)
                w.stateChanged.connect(
                    lambda v, k=key: SETTINGS.__setitem__(k, bool(v))
                )
            elif isinstance(value, int):
                w = QSpinBox()
                w.setMaximum(10000)
                w.setValue(value)
                w.valueChanged.connect(
                    lambda v, k=key: SETTINGS.__setitem__(k, v)
                )
            else:
                continue 

            box.addWidget(w, 2)
            settings_layout.addLayout(box)
            self.setting_widgets[key] = w
            
        settings_layout.addStretch()
        scroll.setWidget(settings_widget)
        layout.addWidget(scroll)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def save_and_accept(self):
        save_settings()
        self.accept()

class StatusUpdater(QObject):
    update_status = pyqtSignal(str, str, str, str, str)   
    update_crawling = pyqtSignal(list)
    update_archiving = pyqtSignal(list)

class CrawlerGUI(QWidget):
    def __init__(self):
        super().__init__()
        load_settings()
        self.coordinator = None
        self.worker_thread = None
        self.timer = None
        self.is_running = False
        self.is_paused = False
        self.dark_mode = SETTINGS.get("dark_mode", True)
        self.status_updater = StatusUpdater()
        self.status_updater.update_status.connect(self.update_stats)
        self.status_updater.update_crawling.connect(self.update_crawling_list)
        self.status_updater.update_archiving.connect(self.update_archiving_list)
        
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        self.setWindowTitle("Wayback When")
        self.resize(1000, 700)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        menubar = QMenuBar()
        file_menu = menubar.addMenu("&File")
        
        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)
        
        theme_action = QAction("&Toggle Theme", self)
        theme_action.triggered.connect(self.toggle_theme)
        file_menu.addAction(theme_action)

        main_layout.setMenuBar(menubar)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        main_layout.addLayout(content_layout)

        sidebar = QVBoxLayout()
        sidebar.setSpacing(15)
        sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.addLayout(sidebar, 1)

        # URL
        url_group = QGroupBox("URL Input")
        url_layout = QVBoxLayout(url_group)
        url_layout.setSpacing(10)
        url_layout.setContentsMargins(10, 10, 10, 10)

        url_row = QHBoxLayout()
        url_row.setSpacing(10)
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter URL (e.g., example.com)")
        url_row.addWidget(self.url_entry, 4)
        
        self.add_url_btn = QPushButton("Add URL")
        self.add_url_btn.clicked.connect(self.add_url)
        url_row.addWidget(self.add_url_btn, 1)
        
        url_layout.addLayout(url_row)
        
        self.url_list = QListWidget()
        self.url_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.url_list.setMinimumHeight(100)
        url_layout.addWidget(self.url_list)
        
        control_btn_layout = QHBoxLayout()
        control_btn_layout.setSpacing(8)
        
        self.start_btn = QPushButton("▶ Start")
        self.start_btn.clicked.connect(self.start_crawling)
        control_btn_layout.addWidget(self.start_btn)
        
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.clicked.connect(self.pause)
        self.pause_btn.setEnabled(False)
        control_btn_layout.addWidget(self.pause_btn)
        
        self.resume_btn = QPushButton("⏯ Resume")
        self.resume_btn.clicked.connect(self.resume)
        self.resume_btn.setEnabled(False)
        control_btn_layout.addWidget(self.resume_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        control_btn_layout.addWidget(self.stop_btn)
        
        url_layout.addLayout(control_btn_layout)
        sidebar.addWidget(url_group)

        # Proxy
        proxy_group = QGroupBox("Proxy Configuration")
        proxy_layout = QVBoxLayout(proxy_group)
        proxy_layout.setSpacing(10)
        proxy_layout.setContentsMargins(10, 10, 10, 10)
        
        proxy_label = QLabel("Proxies (one per line):")
        proxy_layout.addWidget(proxy_label)
        
        self.proxy_text = QTextEdit()
        self.proxy_text.setMaximumHeight(60000)
        self.proxy_text.setPlaceholderText("http://user:pass@host:port\nsocks5://user:pass@host:port")
        proxy_layout.addWidget(self.proxy_text)
        
        proxy_btn_layout = QHBoxLayout()
        proxy_btn_layout.setSpacing(8)
        self.save_proxy_btn = QPushButton("Save Proxies")
        self.save_proxy_btn.clicked.connect(self.save_proxies)
        proxy_btn_layout.addWidget(self.save_proxy_btn)
        
        self.clear_proxy_btn = QPushButton("Clear Proxies")
        self.clear_proxy_btn.clicked.connect(self.clear_proxies)
        proxy_btn_layout.addWidget(self.clear_proxy_btn)
        
        proxy_layout.addLayout(proxy_btn_layout)
        sidebar.addWidget(proxy_group)

        stats_group = QGroupBox("Progress Statistics")
        stats_layout = QVBoxLayout(stats_group)
        stats_layout.setSpacing(10)
        stats_layout.setContentsMargins(10, 10, 10, 10)
        
        self.stats = QLabel("Status: Ready | Archived: 0 | Skipped: 0 | Failed: 0 | Total: 0")
        self.stats.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        stats_layout.addWidget(self.stats)
        
        # Progress bar
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(8)
        
        archiving_label = QLabel("Archiving Progress:")
        self.archiving_progress = QProgressBar()
        self.archiving_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0096ff;
                width: 10px;
                margin: 0px;
            }
        """)
        self.archiving_progress.setFormat("%p% (%v/%m)")
        
        progress_layout.addWidget(archiving_label)
        progress_layout.addWidget(self.archiving_progress)
        
        stats_layout.addLayout(progress_layout)
        sidebar.addWidget(stats_group)

        # Right panel
        panel = QVBoxLayout()
        panel.setSpacing(15)
        panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.addLayout(panel, 2)

        # Crawling Queue Group
        crawl_group = QGroupBox("Crawling Queue")
        crawl_layout = QVBoxLayout(crawl_group)
        crawl_layout.setSpacing(5)
        crawl_layout.setContentsMargins(10, 10, 10, 10)
        self.crawl_list = QListWidget()
        self.crawl_list.setMaximumHeight(600000)
        crawl_layout.addWidget(self.crawl_list)
        panel.addWidget(crawl_group)

        # Archiving Queue Group
        archive_group = QGroupBox("Archiving Queue")
        archive_layout = QVBoxLayout(archive_group)
        archive_layout.setSpacing(5)
        archive_layout.setContentsMargins(10, 10, 10, 10)
        self.archive_list = QListWidget()
        self.archive_list.setMaximumHeight(60000)
        archive_layout.addWidget(self.archive_list)
        panel.addWidget(archive_group)
        
        self.update_proxy_display()
        self.apply_theme()

    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()
        self.apply_theme()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        SETTINGS["dark_mode"] = self.dark_mode
        save_settings()
        self.apply_theme()

    def apply_theme(self):
        app = QApplication.instance()
        if self.dark_mode:
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
            dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
            dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(35, 35, 35))
            dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(220, 220, 220))
            dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 220, 220))
            dark_palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
            dark_palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
            dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
            dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 204))
            dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(127, 127, 127))
            
            app.setPalette(dark_palette)
            
            self.setStyleSheet("""
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
        else:
            app.setPalette(QApplication.style().standardPalette())
            self.setStyleSheet("""
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
                QScrollBar:vertical {
                    border: 1px solid #c0c0c0;
                    background: #f0f0f0;
                    width: 15px;
                    margin: 0;
                }
                QScrollBar:horizontal {
                    border: 1px solid #c0c0c0;
                    background: #f0f0f0;
                    height: 15px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #c0c0c0;
                    min-height: 20px;
                    border-radius: 7px;
                }
                QScrollBar::handle:horizontal {
                    background: #c0c0c0;
                    min-width: 20px;
                    border-radius: 7px;
                }
                QScrollBar::add-line, QScrollBar::sub-line {
                    height: 0;
                    width: 0;
                }
            """)

    def add_url(self):
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
        proxy_text = self.proxy_text.toPlainText().strip()
        if not proxy_text:
            SETTINGS["proxies"] = []
            log_message("INFO", "Proxy list cleared", debug_only=True)
            self.update_proxy_display()
            save_settings()
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
        save_settings()

    def clear_proxies(self):
        SETTINGS["proxies"] = []
        self.update_proxy_display()
        save_settings()
        log_message("INFO", "Proxies cleared", debug_only=True)

    def update_proxy_display(self):
        self.proxy_text.setPlainText("\n".join(SETTINGS.get("proxies", [])))

    def start_crawling(self):
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
        self.archiving_progress.setValue(0)
        self.archiving_progress.setMaximum(1)

    def poll_state(self):
        if not self.coordinator:
            return

        crawling_items = []
        if hasattr(self.coordinator, 'crawling_queue'):
            crawling_items = [u[0] for u in list(self.coordinator.crawling_queue)[:20]]
        self.status_updater.update_crawling.emit(crawling_items)

        archiving_items = []
        if hasattr(self.coordinator, 'queue_for_archiving'):
            archiving_items = list(self.coordinator.queue_for_archiving)[:20]
        self.status_updater.update_archiving.emit(archiving_items)
        
        archived_count = getattr(self.coordinator, 'archived_count', 0)
        skipped_count = getattr(self.coordinator, 'skipped_count', 0)
        failed_count = getattr(self.coordinator, 'failed_count', 0)
        total_processed = archived_count + skipped_count + failed_count
        total_links = getattr(self.coordinator, 'total_links_to_archive', max(1, total_processed))
        
        self.archiving_progress.setMaximum(max(1, total_links))
        self.archiving_progress.setValue(min(archived_count + skipped_count + failed_count, total_links))
        status = "Running"
        if self.is_paused:
            status = "Paused"
        elif not self.is_running:
            status = "Stopped"
            
        self.status_updater.update_status.emit(
            status, 
            str(archived_count), 
            str(skipped_count), 
            str(failed_count), 
            str(total_links)
        )

    def update_crawling_list(self, items):
        self.crawl_list.clear()
        for item in items:
            list_item = QListWidgetItem(item)
            list_item.setForeground(QColor("#ff9900"))  # Orange
            self.crawl_list.addItem(list_item)

    def update_archiving_list(self, items):
        self.archive_list.clear()
        for item in items:
            list_item = QListWidgetItem(item)
            list_item.setForeground(QColor("#00cc66"))  # Green
            self.archive_list.addItem(list_item)

    def update_stats(self, status, archived, skipped, failed, total):
        self.stats.setText(
            f"Status: {status} | "
            f"Archived: <span style='color:#00cc66'>{archived}</span> | "
            f"Skipped: <span style='color:#ff9900'>{skipped}</span> | "
            f"Failed: <span style='color:#ff3333'>{failed}</span> | "
            f"Total: {total}"
        )

    def update_button_states(self):
        self.start_btn.setEnabled(not self.is_running)
        self.add_url_btn.setEnabled(True)
        self.pause_btn.setEnabled(self.is_running and not self.is_paused)
        self.resume_btn.setEnabled(self.is_running and self.is_paused)
        self.stop_btn.setEnabled(self.is_running)

def main():
    load_settings()
    
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    gui = CrawlerGUI()
    gui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
