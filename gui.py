import sys
import threading
import json
import importlib
import csv
from pathlib import Path
from collections import deque

from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QObject
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QLabel,
    QCheckBox, QSpinBox, QGroupBox, QScrollArea, QTextEdit, 
    QStyleFactory, QDialog, QDialogButtonBox, QMenu, QMenuBar,
    QProgressBar, QFrame, QListWidgetItem, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox
)
from PyQt6.QtGui import QPalette, QColor, QAction, QFont, QIcon

from urllib.parse import urlparse

from WaybackWhen import SETTINGS, normalize_url, CrawlCoordinator, log_message, get_root_domain

SETTINGS_FILE = "settings.txt"
THEMES_DIR = Path("themes")
TEXTS_DIR = Path("texts")  

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

class TextManager:
    def __init__(self):
        self.texts_dir = TEXTS_DIR
        self.available_texts = self.discover_texts()
        self.current_text = SETTINGS.get("language", "english")
        self.labels = {}
        self.load_current_text()

    def discover_texts(self):
        if not self.texts_dir.exists():
            self.texts_dir.mkdir()
            self.create_english_text()

        texts = [
            f.stem for f in self.texts_dir.glob("*.csv")
            if f.name != "__init__.py"
        ]

        return texts or ["english"]

    def create_english_text(self):
        english_labels = {
            "window_title": "Wayback When",
            "settings_dialog_title": "Settings",
            "url_input_title": "URL Input",
            "url_placeholder": "Enter URL (e.g., example.com)",
            "add_url_btn": "Add URL",
            "url_list_title": "URL List",
            "start_btn": "▶ Start",
            "pause_btn": "⏸ Pause",
            "resume_btn": "⏯ Resume",
            "stop_btn": "⏹ Stop",
            "proxy_config_title": "Proxy Configuration",
            "proxy_placeholder": "http://user:pass@host:port",
            "save_proxy_btn": "Save Proxies",
            "clear_proxy_btn": "Clear Proxies",
            "progress_stats_title": "Progress Statistics",
            "stats_format": "Status: {status} | Archived: {archived} | Skipped: {skipped} | Failed: {failed} | Total: {total}",
            "crawling_queue_title": "Crawling Queue",
            "archiving_queue_title": "Archiving Queue",
            "file_menu": "&File",
            "settings_action": "&Settings",
            "themes_menu": "&Themes",
            "texts_menu": "&Languages",
            "proxy_label": "Proxies (one per line):",
            "archiving_progress_label": "Archiving Progress:",
            "text_editor_action": "&Change Languages",
            "menu_button": "Menu",
            "no_urls_warning": "No URLs to process",
            "crawler_running_warning": "Crawler is already running",
            "settings_button_tooltip": "Open Menu"
        }
        
        try:
            with open(self.texts_dir / "english.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Key", "Value"])
                for key, value in english_labels.items():
                    writer.writerow([key, value])
            log_message("INFO", "Created english text configuration", True)
        except Exception as e:
            log_message("ERROR", f"Failed to create english text: {e}", False)

    def load_current_text(self):
        text_file = self.texts_dir / f"{self.current_text}.csv"
        if not text_file.exists():
            self.create_english_text()
            text_file = self.texts_dir / "english.csv"
            
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                self.labels = {row[0]: row[1] for row in reader if len(row) >= 2}
        except Exception as e:
            log_message("ERROR", f"Failed to load text config: {e}", False)
            self.labels = {}

    def get_text(self, key, **kwargs):
        text = self.labels.get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        return text

    def set_language(self, language_name):
        self.current_text = language_name
        SETTINGS["language"] = language_name
        save_settings()
        self.load_current_text()

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(parent.text_manager.get_text("settings_dialog_title"))
        self.setMinimumSize(800, 800)
        
        layout = QVBoxLayout(self)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setSpacing(10)
        
        self.setting_widgets = {}
        
        for key, value in SETTINGS.items():
            if key in ["proxies", "language", "theme", "recent_urls"]:
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
        self.text_manager = TextManager()
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
        self.setWindowTitle(self.text_manager.get_text("window_title"))
        self.resize(1400, 1080)
        self.setObjectName("main_window")

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Create menu button
        self.settings_button = QPushButton(self.text_manager.get_text("menu_button"))
        self.settings_button.setObjectName("settings_button")
        self.settings_button.setFixedSize(80, 32)
        self.settings_button.setToolTip(self.text_manager.get_text("settings_button_tooltip"))
        
        # Create menu and actions
        self.settings_menu = QMenu(self)
        self.settings_action = QAction(self.text_manager.get_text("settings_action"), self)
        self.settings_action.triggered.connect(self.show_settings)
        
        self.themes_action = QAction(self.text_manager.get_text("themes_menu"), self)
        self.themes_action.triggered.connect(self.show_themes_menu)
        
        self.languages_action = QAction(self.text_manager.get_text("texts_menu"), self)
        self.languages_action.triggered.connect(self.show_languages_menu)
        
        self.settings_menu.addAction(self.settings_action)
        self.settings_menu.addAction(self.themes_action)
        self.settings_menu.addAction(self.languages_action)
        
        self.settings_button.setMenu(self.settings_menu)
        
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(self.settings_button)
        main_layout.addLayout(top_bar)

        # Main content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        main_layout.addLayout(content_layout)

        # Left sidebar
        sidebar = QVBoxLayout()
        sidebar.setSpacing(15)
        sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.addLayout(sidebar, 1)

        # URL Input Group
        url_group = QGroupBox(self.text_manager.get_text("url_input_title"))
        url_group.setObjectName("url_group")
        url_layout = QVBoxLayout(url_group)
        url_layout.setSpacing(10)
        url_layout.setContentsMargins(10, 10, 10, 10)

        url_row = QHBoxLayout()
        url_row.setSpacing(10)
        
        self.url_combo = QComboBox()
        self.url_combo.setEditable(True)
        self.url_combo.setInsertPolicy(QComboBox.InsertPolicy.InsertAtTop)
        self.url_combo.setDuplicatesEnabled(False)
        self.url_combo.lineEdit().setPlaceholderText(self.text_manager.get_text("url_placeholder"))
        recent_urls = SETTINGS.get("recent_urls", [])
        if recent_urls:
            self.url_combo.addItems(recent_urls)
        url_row.addWidget(self.url_combo, 4)
        
        self.add_url_btn = QPushButton(self.text_manager.get_text("add_url_btn"))
        self.add_url_btn.clicked.connect(self.add_url)
        url_row.addWidget(self.add_url_btn, 1)
        
        url_layout.addLayout(url_row)
        
        self.url_list = QListWidget()
        self.url_list.setMinimumHeight(100)
        url_layout.addWidget(self.url_list)
        
        # Control buttons
        control_btn_layout = QHBoxLayout()
        control_btn_layout.setSpacing(8)
        
        self.start_btn = QPushButton(self.text_manager.get_text("start_btn"))
        self.start_btn.clicked.connect(self.start_crawling)
        control_btn_layout.addWidget(self.start_btn)
        
        self.pause_btn = QPushButton(self.text_manager.get_text("pause_btn"))
        self.pause_btn.clicked.connect(self.pause)
        self.pause_btn.setEnabled(False)
        control_btn_layout.addWidget(self.pause_btn)
        
        self.resume_btn = QPushButton(self.text_manager.get_text("resume_btn"))
        self.resume_btn.clicked.connect(self.resume)
        self.resume_btn.setEnabled(False)
        control_btn_layout.addWidget(self.resume_btn)
        
        self.stop_btn = QPushButton(self.text_manager.get_text("stop_btn"))
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        control_btn_layout.addWidget(self.stop_btn)
        
        url_layout.addLayout(control_btn_layout)
        sidebar.addWidget(url_group)

        # Proxy Configuration Group
        proxy_group = QGroupBox(self.text_manager.get_text("proxy_config_title"))
        proxy_layout = QVBoxLayout(proxy_group)
        proxy_layout.setSpacing(10)
        proxy_layout.setContentsMargins(10, 10, 10, 10)
        
        proxy_label = QLabel(self.text_manager.get_text("proxy_label"))
        proxy_layout.addWidget(proxy_label)
        
        self.proxy_text = QTextEdit()
        self.proxy_text.setPlaceholderText(self.text_manager.get_text("proxy_placeholder"))
        proxy_layout.addWidget(self.proxy_text)
        
        proxy_btn_layout = QHBoxLayout()
        proxy_btn_layout.setSpacing(8)
        self.save_proxy_btn = QPushButton(self.text_manager.get_text("save_proxy_btn"))
        self.save_proxy_btn.clicked.connect(self.save_proxies)
        proxy_btn_layout.addWidget(self.save_proxy_btn)
        
        self.clear_proxy_btn = QPushButton(self.text_manager.get_text("clear_proxy_btn"))
        self.clear_proxy_btn.clicked.connect(self.clear_proxies)
        proxy_btn_layout.addWidget(self.clear_proxy_btn)
        
        proxy_layout.addLayout(proxy_btn_layout)
        sidebar.addWidget(proxy_group)

        # Progress Statistics Group
        stats_group = QGroupBox(self.text_manager.get_text("progress_stats_title"))
        stats_layout = QVBoxLayout(stats_group)
        stats_layout.setSpacing(10)
        stats_layout.setContentsMargins(10, 10, 10, 10)
        
        self.stats = QLabel(self.text_manager.get_text("stats_format", 
                                                     status="Ready", 
                                                     archived="0", 
                                                     skipped="0", 
                                                     failed="0", 
                                                     total="0"))
        self.stats.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        stats_layout.addWidget(self.stats)
        
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(8)
        
        archiving_label = QLabel(self.text_manager.get_text("archiving_progress_label"))
        self.archiving_progress = QProgressBar()
        self.archiving_progress.setFormat("%p% (%v/%m)")
        
        progress_layout.addWidget(archiving_label)
        progress_layout.addWidget(self.archiving_progress)
        
        stats_layout.addLayout(progress_layout)
        sidebar.addWidget(stats_group)

        # Right panel with queues
        panel = QVBoxLayout()
        panel.setSpacing(15)
        panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.addLayout(panel, 2)

        # Crawling Queue
        crawl_group = QGroupBox(self.text_manager.get_text("crawling_queue_title"))
        crawl_layout = QVBoxLayout(crawl_group)
        crawl_layout.setContentsMargins(10, 10, 10, 10)
        self.crawl_list = QListWidget()
        crawl_layout.addWidget(self.crawl_list)
        panel.addWidget(crawl_group)

        # Archiving Queue
        archive_group = QGroupBox(self.text_manager.get_text("archiving_queue_title"))
        archive_layout = QVBoxLayout(archive_group)
        archive_layout.setContentsMargins(10, 10, 10, 10)
        self.archive_list = QListWidget()
        archive_layout.addWidget(self.archive_list)
        panel.addWidget(archive_group)
        
        # Load saved proxies
        self.update_proxy_display()
        self.apply_theme()

    def show_themes_menu(self):
        menu = QMenu(self)
        for theme in self.theme_manager.available_themes:
            action = menu.addAction(theme.capitalize())
            action.triggered.connect(lambda checked, t=theme: self.set_theme(t))
        menu.exec(self.settings_button.mapToGlobal(self.settings_button.rect().bottomLeft()))

    def show_languages_menu(self):
        menu = QMenu(self)
        for text in self.text_manager.available_texts:
            action = menu.addAction(text.capitalize())
            action.triggered.connect(lambda checked, t=text: self.set_language(t))
        menu.exec(self.settings_button.mapToGlobal(self.settings_button.rect().bottomLeft()))

    def set_theme(self, theme_name):
        self.current_theme = theme_name
        SETTINGS["theme"] = theme_name
        save_settings()
        self.apply_theme()

    def set_language(self, language_name):
        self.text_manager.set_language(language_name)
        self.update_ui_texts()

    def apply_theme(self):
        app = QApplication.instance()
        self.theme_manager.apply_theme(self.current_theme, app, self)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.apply_theme()

    def update_ui_texts(self):
        """Update all UI texts when language changes"""
        self.setWindowTitle(self.text_manager.get_text("window_title"))
        self.settings_button.setText(self.text_manager.get_text("menu_button"))
        self.settings_button.setToolTip(self.text_manager.get_text("settings_button_tooltip"))
        self.settings_action.setText(self.text_manager.get_text("settings_action"))
        self.themes_action.setText(self.text_manager.get_text("themes_menu"))
        self.languages_action.setText(self.text_manager.get_text("texts_menu"))
        
        # Update group boxes
        for group in self.findChildren(QGroupBox):
            if group.objectName() == "url_group":
                group.setTitle(self.text_manager.get_text("url_input_title"))
            elif group.objectName() == "proxy_group":
                group.setTitle(self.text_manager.get_text("proxy_config_title"))
            elif group.objectName() == "stats_group":
                group.setTitle(self.text_manager.get_text("progress_stats_title"))
            elif group.objectName() == "crawl_group":
                group.setTitle(self.text_manager.get_text("crawling_queue_title"))
            elif group.objectName() == "archive_group":
                group.setTitle(self.text_manager.get_text("archiving_queue_title"))
        
        # Update buttons
        self.add_url_btn.setText(self.text_manager.get_text("add_url_btn"))
        self.start_btn.setText(self.text_manager.get_text("start_btn"))
        self.pause_btn.setText(self.text_manager.get_text("pause_btn"))
        self.resume_btn.setText(self.text_manager.get_text("resume_btn"))
        self.stop_btn.setText(self.text_manager.get_text("stop_btn"))
        self.save_proxy_btn.setText(self.text_manager.get_text("save_proxy_btn"))
        self.clear_proxy_btn.setText(self.text_manager.get_text("clear_proxy_btn"))
        
        # Update placeholders and labels
        self.url_combo.lineEdit().setPlaceholderText(self.text_manager.get_text("url_placeholder"))
        self.proxy_text.setPlaceholderText(self.text_manager.get_text("proxy_placeholder"))
        for label in self.findChildren(QLabel):
            if label.text().startswith("Proxies"):
                label.setText(self.text_manager.get_text("proxy_label"))
            elif label.text().startswith("Archiving"):
                label.setText(self.text_manager.get_text("archiving_progress_label"))

    def add_url(self):
        url = self.url_combo.currentText().strip()
        if not url:
            return
            
        if "://" not in url:
            url = "http://" + url
            
        if not any(self.url_list.item(i).text() == url for i in range(self.url_list.count())):
            self.url_list.addItem(url)
            
        # Update recent URLs
        recent_urls = SETTINGS.get("recent_urls", [])
        if url in recent_urls:
            recent_urls.remove(url)
        recent_urls.insert(0, url)
        SETTINGS["recent_urls"] = recent_urls[:10]
        save_settings()
        
        # Update combo box
        self.url_combo.clear()
        self.url_combo.addItems(recent_urls)
        self.url_combo.setCurrentText("")
        
        # Add to running crawler if active
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
                        continue
                    proxies.append(proxy)
                except:
                    continue

        SETTINGS["proxies"] = proxies
        self.update_proxy_display()
        save_settings()

    def clear_proxies(self):
        SETTINGS["proxies"] = []
        self.update_proxy_display()
        save_settings()

    def update_proxy_display(self):
        self.proxy_text.setPlainText("\n".join(SETTINGS.get("proxies", [])))

    def start_crawling(self):
        if self.url_list.count() == 0:
            log_message("WARNING", self.text_manager.get_text("no_urls_warning"), debug_only=False)
            return
            
        self.save_proxies()

        if self.worker_thread and self.worker_thread.is_alive():
            log_message("INFO", self.text_manager.get_text("crawler_running_warning"), debug_only=False)
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
            list_item.setForeground(QColor("#ff9900"))
            self.crawl_list.addItem(list_item)

    def update_archiving_list(self, items):
        self.archive_list.clear()
        for item in items:
            list_item = QListWidgetItem(item)
            list_item.setForeground(QColor("#00cc66"))
            self.archive_list.addItem(list_item)

    def update_stats(self, status, archived, skipped, failed, total):
        formatted_text = self.text_manager.get_text("stats_format",
                                                  status=status,
                                                  archived=archived,
                                                  skipped=skipped,
                                                  failed=failed,
                                                  total=total)
        self.stats.setText(formatted_text)

    def update_button_states(self):
        self.start_btn.setEnabled(not self.is_running)
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
