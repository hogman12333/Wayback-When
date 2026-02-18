import sys
import threading
import json
import importlib
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
THEMES_DIR = Path("themes")

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
            SETTINGS["theme"] = "dark"
            save_settings()
    except Exception as e:
        log_message("ERROR", f"Failed to load settings: {str(e)}", debug_only=False)
        SETTINGS["theme"] = "dark"
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
            label.setObjectName(f"{key}_label")
            box.addWidget(label, 1)

            if isinstance(value, bool):
                w = QCheckBox()
                w.setChecked(value)
                w.stateChanged.connect(
                    lambda v, k=key: SETTINGS.__setitem__(k, bool(v))
                )
                w.setObjectName(f"{key}_checkbox")
            elif isinstance(value, int):
                w = QSpinBox()
                w.setMaximum(10000)
                w.setValue(value)
                w.valueChanged.connect(
                    lambda v, k=key: SETTINGS.__setitem__(k, v)
                )
                w.setObjectName(f"{key}_spinbox")
            else:
                w = QLineEdit(str(value))
                w.textChanged.connect(
                    lambda v, k=key: SETTINGS.__setitem__(k, v)
                )
                w.setObjectName(f"{key}_lineedit")

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

class ThemeManager:
    def __init__(self):
        self.available_themes = self.discover_themes()

    def discover_themes(self):
        if not THEMES_DIR.exists():
            THEMES_DIR.mkdir()

        themes = [
            f.stem for f in THEMES_DIR.glob("*.py")
            if f.name != "__init__.py"
        ]

        return themes or ["dark"]

    def apply_theme(self, theme_name, app, widget):
        try:
            module = importlib.import_module(f"themes.{theme_name}")
            importlib.reload(module)
            module.apply(app, widget)
        except Exception as e:
            log_message("ERROR", f"Theme load failed: {e}", False)

class StatusUpdater(QObject):
    update_status = pyqtSignal(str, str, str, str, str)   
    update_crawling = pyqtSignal(list)
    update_archiving = pyqtSignal(list)

class CrawlerGUI(QWidget):
    def __init__(self):
        super().__init__()
        load_settings()
        
        self.theme_manager = ThemeManager()
        self.current_theme = SETTINGS.get("theme", "dark")

        self.coordinator = None
        self.worker_thread = None
        self.timer = None
        self.is_running = False
        self.is_paused = False
        self.status_updater = StatusUpdater()
        self.status_updater.update_status.connect(self.update_stats)
        self.status_updater.update_crawling.connect(self.update_crawling_list)
        self.status_updater.update_archiving.connect(self.update_archiving_list)
        
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        self.setWindowTitle("Wayback When")
        self.resize(1000, 700)
        self.setObjectName("main_window")

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        menubar = QMenuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.setObjectName("file_menu")
        
        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.show_settings)
        settings_action.setObjectName("settings_action")
        file_menu.addAction(settings_action)
        
        theme_menu = menubar.addMenu("&Themes")
        theme_menu.setObjectName("theme_menu")
        self.populate_theme_menu(theme_menu)

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
        url_group.setObjectName("url_group")
        url_layout = QVBoxLayout(url_group)
        url_layout.setSpacing(10)
        url_layout.setContentsMargins(10, 10, 10, 10)

        url_row = QHBoxLayout()
        url_row.setSpacing(10)
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter URL (e.g., example.com)")
        self.url_entry.setObjectName("url_entry")
        self.url_entry.setAccessibleName("URL Entry Field")
        self.url_entry.setAccessibleDescription("Enter a website URL to begin archiving")
        url_row.addWidget(self.url_entry, 4)
        
        self.add_url_btn = QPushButton("Add URL")
        self.add_url_btn.clicked.connect(self.add_url)
        self.add_url_btn.setObjectName("add_url_btn")
        self.add_url_btn.setAccessibleName("Add URL Button")
        self.add_url_btn.setAccessibleDescription("Adds the entered URL to the processing queue")
        url_row.addWidget(self.add_url_btn, 1)
        
        url_layout.addLayout(url_row)
        
        self.url_list = QListWidget()
        self.url_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.url_list.setMinimumHeight(100)
        self.url_list.setObjectName("url_list")
        self.url_list.setAccessibleName("URL List")
        self.url_list.setAccessibleDescription("List of URLs to be processed")
        url_layout.addWidget(self.url_list)
        
        control_btn_layout = QHBoxLayout()
        control_btn_layout.setSpacing(8)
        
        self.start_btn = QPushButton("▶ Start")
        self.start_btn.clicked.connect(self.start_crawling)
        self.start_btn.setObjectName("start_btn")
        self.start_btn.setAccessibleName("Start Button")
        self.start_btn.setAccessibleDescription("Begins the archiving process for all listed URLs")
        control_btn_layout.addWidget(self.start_btn)
        
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.clicked.connect(self.pause)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setObjectName("pause_btn")
        self.pause_btn.setAccessibleName("Pause Button")
        self.pause_btn.setAccessibleDescription("Pauses the current archiving process")
        control_btn_layout.addWidget(self.pause_btn)
        
        self.resume_btn = QPushButton("⏯ Resume")
        self.resume_btn.clicked.connect(self.resume)
        self.resume_btn.setEnabled(False)
        self.resume_btn.setObjectName("resume_btn")
        self.resume_btn.setAccessibleName("Resume Button")
        self.resume_btn.setAccessibleDescription("Resumes the paused archiving process")
        control_btn_layout.addWidget(self.resume_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setObjectName("stop_btn")
        self.stop_btn.setAccessibleName("Stop Button")
        self.stop_btn.setAccessibleDescription("Stops the archiving process completely")
        control_btn_layout.addWidget(self.stop_btn)
        
        url_layout.addLayout(control_btn_layout)
        sidebar.addWidget(url_group)

        # Proxy
        proxy_group = QGroupBox("Proxy Configuration")
        proxy_group.setObjectName("proxy_group")
        proxy_layout = QVBoxLayout(proxy_group)
        proxy_layout.setSpacing(10)
        proxy_layout.setContentsMargins(10, 10, 10, 10)
        
        proxy_label = QLabel("Proxies (one per line):")
        proxy_label.setObjectName("proxy_label")
        proxy_label.setAccessibleName("Proxy Configuration Label")
        proxy_layout.addWidget(proxy_label)
        
        self.proxy_text = QTextEdit()
        self.proxy_text.setMaximumHeight(60000)
        self.proxy_text.setPlaceholderText("http://user:pass@host:port\nsocks5://user:pass@host:port")
        self.proxy_text.setObjectName("proxy_text")
        self.proxy_text.setAccessibleName("Proxy Text Area")
        self.proxy_text.setAccessibleDescription("Enter proxy servers one per line in protocol://user:pass@host:port format")
        proxy_layout.addWidget(self.proxy_text)
        
        proxy_btn_layout = QHBoxLayout()
        proxy_btn_layout.setSpacing(8)
        self.save_proxy_btn = QPushButton("Save Proxies")
        self.save_proxy_btn.clicked.connect(self.save_proxies)
        self.save_proxy_btn.setObjectName("save_proxy_btn")
        self.save_proxy_btn.setAccessibleName("Save Proxies Button")
        self.save_proxy_btn.setAccessibleDescription("Saves the entered proxy configurations")
        proxy_btn_layout.addWidget(self.save_proxy_btn)
        
        self.clear_proxy_btn = QPushButton("Clear Proxies")
        self.clear_proxy_btn.clicked.connect(self.clear_proxies)
        self.clear_proxy_btn.setObjectName("clear_proxy_btn")
        self.clear_proxy_btn.setAccessibleName("Clear Proxies Button")
        self.clear_proxy_btn.setAccessibleDescription("Clears all proxy configurations")
        proxy_btn_layout.addWidget(self.clear_proxy_btn)
        
        proxy_layout.addLayout(proxy_btn_layout)
        sidebar.addWidget(proxy_group)

        stats_group = QGroupBox("Progress Statistics")
        stats_group.setObjectName("stats_group")
        stats_layout = QVBoxLayout(stats_group)
        stats_layout.setSpacing(10)
        stats_layout.setContentsMargins(10, 10, 10, 10)
        
        self.stats = QLabel("Status: Ready | Archived: 0 | Skipped: 0 | Failed: 0 | Total: 0")
        self.stats.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.stats.setObjectName("stats_label")
        self.stats.setAccessibleName("Statistics Display")
        self.stats.setAccessibleDescription("Shows current archiving statistics including status, archived count, skipped count, failed count, and total count")
        stats_layout.addWidget(self.stats)
        
        # Progress bar
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(8)
        
        archiving_label = QLabel("Archiving Progress:")
        archiving_label.setObjectName("archiving_label")
        archiving_label.setAccessibleName("Archiving Progress Label")
        self.archiving_progress = QProgressBar()
        self.archiving_progress.setFormat("%p% (%v/%m)")
        self.archiving_progress.setObjectName("archiving_progress")
        self.archiving_progress.setAccessibleName("Archiving Progress Bar")
        self.archiving_progress.setAccessibleDescription("Visual representation of archiving progress percentage")
        
        progress_layout.addWidget(archiving_label)
        progress_layout.addWidget(self.archiving_progress)
        
        stats_layout.addLayout(progress_layout)
        sidebar.addWidget(stats_group)

        # Right panel
        panel = QVBoxLayout()
        panel.setSpacing(15)
        panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.addLayout(panel, 2)

        # Crawling Queue
        crawl_group = QGroupBox("Crawling Queue")
        crawl_group.setObjectName("crawl_group")
        crawl_layout = QVBoxLayout(crawl_group)
        crawl_layout.setSpacing(5)
        crawl_layout.setContentsMargins(10, 10, 10, 10)
        self.crawl_list = QListWidget()
        self.crawl_list.setObjectName("crawl_list")
        self.crawl_list.setAccessibleName("Crawling Queue List")
        self.crawl_list.setAccessibleDescription("Shows URLs currently being crawled")
        crawl_layout.addWidget(self.crawl_list)
        panel.addWidget(crawl_group)

        # Archiving Queue
        archive_group = QGroupBox("Archiving Queue")
        archive_group.setObjectName("archive_group")
        archive_layout = QVBoxLayout(archive_group)
        archive_layout.setSpacing(5)
        archive_layout.setContentsMargins(10, 10, 10, 10)
        self.archive_list = QListWidget()
        self.archive_list.setObjectName("archive_list")
        self.archive_list.setAccessibleName("Archiving Queue List")
        self.archive_list.setAccessibleDescription("Shows URLs currently being archived")
        archive_layout.addWidget(self.archive_list)
        panel.addWidget(archive_group)
        
        self.update_proxy_display()
        self.apply_theme()

    def populate_theme_menu(self, menu):
        menu.clear()
        for theme in self.theme_manager.available_themes:
            action = QAction(theme.capitalize(), self)
            action.triggered.connect(lambda checked, t=theme: self.set_theme(t))
            menu.addAction(action)

    def set_theme(self, theme_name):
        self.current_theme = theme_name
        SETTINGS["theme"] = theme_name
        save_settings()
        self.apply_theme()

    def apply_theme(self):
        app = QApplication.instance()
        self.theme_manager.apply_theme(self.current_theme, app, self)
        # Force repaint to ensure theme changes are applied
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.apply_theme()

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
