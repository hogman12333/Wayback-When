import sys
import threading
import json
from pathlib import Path

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QLabel,
    QCheckBox, QSpinBox, QGroupBox, QScrollArea, QTextEdit, 
    QStyleFactory, QDialog, QDialogButtonBox, QMenu, QMenuBar,
    QStyle
)
from PyQt6.QtGui import QPalette, QColor, QAction, QIcon

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
    except Exception as e:
        log_message("ERROR", f"Failed to load settings: {str(e)}", debug_only=False)

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
                w.setMaximum(10_000)
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

class CrawlerGUI(QWidget):
    def __init__(self):
        super().__init__()
        load_settings()
        self.coordinator = None
        self.worker_thread = None
        self.timer = None
        self.is_running = False
        self.is_paused = False
        self.dark_mode = SETTINGS.get("dark_mode", False)

        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        self.setWindowTitle("Wayback When")
        self.resize(1200, 700)

        menubar = QMenuBar(self)
        file_menu = menubar.addMenu("&File")
        
        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)
        
        theme_action = QAction("&Toggle Theme", self)
        theme_action.triggered.connect(self.toggle_theme)
        file_menu.addAction(theme_action)

        root = QVBoxLayout()
        root.setMenuBar(menubar)
        self.setLayout(root)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        root.addLayout(main_layout)

        sidebar = QVBoxLayout()
        sidebar.setSpacing(10)
        main_layout.addLayout(sidebar, 1)

        url_group = QGroupBox("")
        url_layout = QVBoxLayout()
        url_layout.setSpacing(8)

        url_row = QHBoxLayout()
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter URL (e.g., example.com)")
        url_row.addWidget(self.url_entry, 4)
        
        self.add_url_btn = QPushButton("Add")
        self.add_url_btn.setFixedWidth(80)
        self.add_url_btn.clicked.connect(self.add_url)
        url_row.addWidget(self.add_url_btn, 1)
        
        url_layout.addLayout(url_row)
        
        self.url_list = QListWidget()
        self.url_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        url_layout.addWidget(self.url_list, 2)
        
        control_btn_layout = QHBoxLayout()
        control_btn_layout.setSpacing(5)
        
        self.start_btn = QPushButton("Start")
        self.start_btn.setFixedWidth(80)
        self.start_btn.clicked.connect(self.start_crawling)
        control_btn_layout.addWidget(self.start_btn)
        
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setFixedWidth(80)
        self.pause_btn.clicked.connect(self.pause)
        self.pause_btn.setEnabled(False)
        control_btn_layout.addWidget(self.pause_btn)
        
        self.resume_btn = QPushButton("Resume")
        self.resume_btn.setFixedWidth(80)
        self.resume_btn.clicked.connect(self.resume)
        self.resume_btn.setEnabled(False)
        control_btn_layout.addWidget(self.resume_btn)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setFixedWidth(80)
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        control_btn_layout.addWidget(self.stop_btn)
        
        url_layout.addLayout(control_btn_layout)
        url_group.setLayout(url_layout)
        sidebar.addWidget(url_group, 1)

        proxy_group = QGroupBox("")
        proxy_layout = QVBoxLayout()
        proxy_layout.setSpacing(8)
        
        proxy_label = QLabel("Proxies (one per line):")
        proxy_layout.addWidget(proxy_label)
        
        self.proxy_text = QTextEdit()
        self.proxy_text.setMaximumHeight(120)
        self.proxy_text.setPlaceholderText("http://user:pass@host:port\nsocks5://user:pass@host:port")
        proxy_layout.addWidget(self.proxy_text)
        
        proxy_btn_layout = QHBoxLayout()
        proxy_btn_layout.setSpacing(5)
        self.save_proxy_btn = QPushButton("Save")
        self.save_proxy_btn.setFixedWidth(80)
        self.save_proxy_btn.clicked.connect(self.save_proxies)
        proxy_btn_layout.addWidget(self.save_proxy_btn)
        
        self.clear_proxy_btn = QPushButton("Clear")
        self.clear_proxy_btn.setFixedWidth(80)
        self.clear_proxy_btn.clicked.connect(self.clear_proxies)
        proxy_btn_layout.addWidget(self.clear_proxy_btn)
        
        proxy_layout.addLayout(proxy_btn_layout)
        proxy_group.setLayout(proxy_layout)
        sidebar.addWidget(proxy_group)

        stats_box = QGroupBox("")
        stats_layout = QVBoxLayout()
        self.stats = QLabel("Status: Ready | Archived: 0 | Skipped: 0 | Failed: 0 | Total: 0")
        stats_layout.addWidget(self.stats)
        stats_box.setLayout(stats_layout)
        sidebar.addWidget(stats_box)

        panel = QVBoxLayout()
        panel.setSpacing(10)
        main_layout.addLayout(panel, 2)

        crawl_group = QGroupBox("")
        crawl_layout = QVBoxLayout()
        self.crawl_list = QListWidget()
        crawl_layout.addWidget(self.crawl_list)
        crawl_group.setLayout(crawl_layout)
        panel.addWidget(crawl_group, 1)

        archive_group = QGroupBox("")
        archive_layout = QVBoxLayout()
        self.archive_list = QListWidget()
        archive_layout.addWidget(self.archive_list)
        archive_group.setLayout(archive_layout)
        panel.addWidget(archive_group, 1)
        
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
            dark_palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 48))
            dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240))
            dark_palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
            dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 48))
            dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(240, 240, 240))
            dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(240, 240, 240))
            dark_palette.setColor(QPalette.ColorRole.Text, QColor(240, 240, 240))
            dark_palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 48))
            dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 240, 240))
            dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 204))
            dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(127, 127, 127))
            
            app.setPalette(dark_palette)
            
            self.setStyleSheet("""
                QWidget {
                    font-size: 11pt;
                    color: #d4d4d4;
                    background-color: #2d2d30;
                }
                QGroupBox {
                    border: 1px solid #3f3f46;
                    border-radius: 15px;
                    margin-top: 0.5em;
                    padding-top: 10px;
                    background-color: #2d2d30;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 6px 0 6px;
                    color: #e1e1e1;
                    background-color: transparent;
                }
                QListWidget, QTextEdit, QLineEdit {
                    background-color: #252526;
                    color: #d4d4d4;
                    border: 1px solid #3f3f46;
                    border-radius: 3px;
                    padding: 4px;
                    selection-background-color: #007acc;
                    selection-color: white;
                }
                QPushButton {
                    background-color: #333337;
                    color: #d4d4d4;
                    border: 1px solid #3f3f46;
                    border-radius: 3px;
                    padding: 5px 10px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #2a2a2f;
                    border-color: #5f5f67;
                }
                QPushButton:pressed {
                    background-color: #1e1e1e;
                }
                QPushButton:disabled {
                    color: #777;
                    background-color: #2d2d30;
                }
                QMenuBar {
                    background-color: #2d2d30;
                    color: #d4d4d4;
                    border-bottom: 1px solid #3f3f46;
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
                    color: #d4d4d4;
                    border: 1px solid #3f3f46;
                }
                QMenu::item:selected {
                    background-color: #3e3e40;
                }
                QScrollBar:vertical {
                    border: 1px solid #3f3f46;
                    background: #2d2d30;
                    width: 12px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #3e3e40;
                    min-height: 20px;
                    border-radius: 5px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0;
                }
            """)
        else:
            app.setPalette(QApplication.style().standardPalette())
            self.setStyleSheet("""
                QWidget {
                    font-size: 11pt;
                }
                QGroupBox {
                    border: 1px solid #c0c0c0;
                    border-radius: 5px;
                    margin-top: 0.5em;
                    padding-top: 10px;
                    background-color: white;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 6px 0 6px;
                    background-color: transparent;
                }
                QListWidget, QTextEdit, QLineEdit {
                    border: 1px solid #c0c0c0;
                    border-radius: 3px;
                    padding: 4px;
                    background-color: white;
                    color: black;
                    selection-background-color: #0078d7;
                    selection-color: white;
                }
                QPushButton {
                    padding: 5px 10px;
                    border-radius: 3px;
                    border: 1px solid #c0c0c0;
                    background-color: #f0f0f0;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
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
                    width: 12px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #c0c0c0;
                    min-height: 20px;
                    border-radius: 5px;
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

    def poll_state(self):
        if not self.coordinator:
            return

        self.crawl_list.clear()
        if hasattr(self.coordinator, 'crawling_queue'):
            self.crawl_list.addItems(
                [u[0] for u in self.coordinator.crawling_queue]
            )

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
