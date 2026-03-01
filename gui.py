import sys
import threading
import json
import importlib
import csv
from pathlib import Path
from collections import deque
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QObject, QSize
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPalette, QColor, QAction, QFont, QIcon, QPixmap
from urllib.parse import urlparse
from WaybackWhen import SETTINGS, CrawlCoordinator, log_message

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
            "themes_dialog_title": "Themes",
            "url_input_title": "URL Input",
            "proxy_config_title": "Proxy Configuration",
            "progress_stats_title": "Progress Statistics",
            "crawling_queue_title": "Crawling Queue",
            "archiving_queue_title": "Archiving Queue",
            "add_url_btn": "Add URL",
            "start_btn": "▶ Start",
            "pause_btn": "⏸ Pause",
            "resume_btn": "⏯ Resume",
            "stop_btn": "⏹ Stop",
            "save_proxy_btn": "Save Proxies",
            "clear_proxy_btn": "Clear Proxies",
            "apply_theme_btn": "Apply",
            "file_menu": "  &File",
            "settings_action": "  &Settings",
            "themes_menu": "  &Themes",
            "texts_menu": "  &Languages",
            "text_editor_action": "  &Change Languages",
            "url_placeholder": "Enter URL (e.g., example.com)",
            "proxy_label": "Proxies (one per line):",
            "archiving_progress_label": "Archiving Progress:",
            "stats_format": "Status: {status} | Archived: {archived} | Skipped: {skipped} | Failed: {failed} | Total: {total}",
            "no_urls_warning": "No URLs to process",
            "crawler_running_warning": "Crawler is already running",
            "settings_button_tooltip": "Open Menu",
            "theme_preview_unavailable": "No preview\navailable",
            "theme_preview_failed": "Failed to load image",
            "themes_title": "Themes",
            "theme_apply_button": "Apply",
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
                next(reader)
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
                w.stateChanged.connect(lambda v, k=key: SETTINGS.__setitem__(k, bool(v)))
                w.setObjectName(f"{key}_checkbox")
            elif isinstance(value, int):
                w = QSpinBox()
                w.setMaximum(10000)
                w.setValue(value)
                w.valueChanged.connect(lambda v, k=key: SETTINGS.__setitem__(k, v))
                w.setObjectName(f"{key}_spinbox")
            else:
                w = QLineEdit(str(value))
                w.textChanged.connect(lambda v, k=key: SETTINGS.__setitem__(k, v))
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


class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme_name = None
        self.dialog = None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.open_preview_window()
        super().mousePressEvent(event)

    def open_preview_window(self):
        if self.theme_name and self.dialog:
            self.dialog.show_theme_preview(self.theme_name)


class ThemeMarketDialog(QDialog):
    def __init__(self, theme_manager, current_theme, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.current_theme = current_theme
        self.parent_gui = parent
        self.text_manager = parent.text_manager
        self.current_preview_theme = None
        self.setWindowTitle(self.text_manager.get_text("themes_dialog_title"))
        self.resize(1200, 800)
        self.setMinimumSize(800, 600)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with back button
        header_layout = QHBoxLayout()
        self.back_button = QPushButton("← Back")
        self.back_button.setFixedSize(80, 30)
        self.back_button.clicked.connect(self.show_theme_grid)
        self.back_button.setVisible(False)
        header_layout.addWidget(self.back_button)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Stacked widget for grid/preview views
        self.stack = QStackedWidget()
        #theme grid
        self.grid_page = QWidget()
        grid_layout = QVBoxLayout(self.grid_page)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.grid_layout.setSpacing(20)
        self.scroll_area.setWidget(self.scroll_widget)
        grid_layout.addWidget(self.scroll_area)
        
        self.stack.addWidget(self.grid_page)
        
        # Theme Preview
        self.preview_page = QWidget()
        preview_layout = QVBoxLayout(self.preview_page)
        preview_layout.setSpacing(15)
        preview_layout.setContentsMargins(20, 20, 20, 20)
        
        self.preview_title = QLabel("")
        self.preview_title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.preview_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self.preview_title)
        
        self.preview_image = QLabel()
        self.preview_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_image.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")
        self.preview_image.setFixedSize(600, 400)
        preview_layout.addWidget(self.preview_image)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setStyleSheet("font-size: 14px; padding: 10px;")
        preview_layout.addWidget(self.preview_text)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.preview_apply_button = QPushButton(self.text_manager.get_text("theme_apply_button"))
        self.preview_apply_button.setFixedSize(120, 35)
        self.preview_apply_button.clicked.connect(self.apply_current_preview_theme)
        button_layout.addWidget(self.preview_apply_button)
        button_layout.addStretch()
        preview_layout.addLayout(button_layout)
        
        self.stack.addWidget(self.preview_page)
        layout.addWidget(self.stack)
        
        # Close button (only on grid view)
        self.close_button_layout = QHBoxLayout()
        self.close_button_layout.addStretch()
        self.close_button = QPushButton("Close")
        self.close_button.setFixedSize(100, 30)
        self.close_button.clicked.connect(self.accept)
        self.close_button_layout.addWidget(self.close_button)
        layout.addLayout(self.close_button_layout)
        
        self.populate_themes()

    def populate_themes(self):
        # Clear existing widgets
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        themes = self.theme_manager.available_themes
        if not themes:
            no_themes_label = QLabel("No themes available")
            no_themes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(no_themes_label, 0, 0)
            return
        
        # Calculate columns based on dialog width
        dialog_width = max(800, self.width())
        min_column_width = 300
        columns = max(1, min(len(themes), dialog_width // min_column_width))
        
        for i in range(columns):
            self.grid_layout.setColumnStretch(i, 1)
        
        row, col = 0, 0
        for theme_name in themes:
            theme_widget = self.create_theme_widget(theme_name)
            self.grid_layout.addWidget(theme_widget, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1

    def create_theme_widget(self, theme_name):
        widget = QWidget()
        widget.setObjectName("theme_card")
        
        # Calculate card size
        dialog_width = max(800, self.width())
        columns = max(1, dialog_width // 300)
        card_width = max(200, (dialog_width - 100) // columns - 20)
        card_height = int(card_width * 1.3)
        
        widget.setFixedSize(card_width, card_height)
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Theme name label
        theme_label = QLabel(theme_name.capitalize())
        theme_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        theme_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(theme_label)
        
        # Image label (clickable)
        image_label = ClickableLabel()
        image_label.theme_name = theme_name
        image_label.dialog = self
        
        image_height = int(card_height * 0.7)
        image_label.setFixedSize(card_width - 20, image_height)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")
        image_label.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Load theme image
        image_path = self.get_theme_image_path(theme_name)
        if image_path and image_path.exists():
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                image_label.setPixmap(
                    pixmap.scaled(
                        card_width - 20, image_height,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
            else:
                image_label.setText(self.text_manager.get_text("theme_preview_failed"))
        else:
            image_label.setText(self.text_manager.get_text("theme_preview_unavailable"))
        
        layout.addWidget(image_label)
        
        # Buttons
        view_button = QPushButton("View")
        view_button.setFixedSize(50, 22)
        view_button.clicked.connect(lambda _, t=theme_name: self.show_theme_preview(t))
        
        apply_button = QPushButton(self.text_manager.get_text("theme_apply_button"))
        apply_button.setFixedSize(50, 22)
        apply_button.clicked.connect(lambda _, t=theme_name: self.apply_theme(t))
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        button_layout.addStretch()
        button_layout.addWidget(view_button)
        button_layout.addWidget(apply_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        
        return widget

    def show_theme_preview(self, theme_name):
        self.current_preview_theme = theme_name
        
        # Update title
        self.preview_title.setText(f"Preview: {theme_name.capitalize()}")
        
        # Load image
        image_path = self.get_theme_image_path(theme_name)
        if image_path and image_path.exists():
            pixmap = QPixmap(str(image_path))
            if not pixmap.isNull():
                self.preview_image.setPixmap(
                    pixmap.scaled(
                        600, 400,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
            else:
                self.preview_image.setText(self.text_manager.get_text("theme_preview_failed"))
        else:
            self.preview_image.setText(self.text_manager.get_text("theme_preview_unavailable"))
        
        # Load text content
        text_path = THEMES_DIR / f"{theme_name}.txt"
        
        if not text_path.exists():
            try:
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(f"Theme: {theme_name}\n\nThis is the description for the {theme_name} theme.\nYou can edit this file to add your own content.")
                log_message("INFO", f"Created text file for theme: {theme_name}", debug_only=True)
            except Exception as e:
                log_message("ERROR", f"Failed to create text file: {str(e)}", debug_only=False)
        
        if text_path.exists():
            try:
                with open(text_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.preview_text.setText(content)
            except Exception as e:
                self.preview_text.setText(f"Error loading text: {str(e)}")
        else:
            self.preview_text.setText(f"No preview text available.\nCreate '{theme_name}.txt' in the themes folder.")
        
        # Switch to preview page
        self.stack.setCurrentIndex(1)
        self.back_button.setVisible(True)
        self.close_button.setVisible(False)

    def show_theme_grid(self):
        self.stack.setCurrentIndex(0)
        self.back_button.setVisible(False)
        self.close_button.setVisible(True)
        self.current_preview_theme = None

    def apply_current_preview_theme(self):
        if self.current_preview_theme:
            self.apply_theme(self.current_preview_theme)

    def apply_theme(self, theme_name):
        self.parent_gui.set_theme(theme_name)
        self.current_theme = theme_name
        self.populate_themes()

    def get_theme_image_path(self, theme_name):
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
        for ext in image_extensions:
            path = THEMES_DIR / f"{theme_name}{ext}"
            if path.exists():
                return path
        return None


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
        self.resize(1200, 1200)
        self.setObjectName("main_window")
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setIconSize(QSize(16, 16))
        
        self.settings_action = QAction(self.text_manager.get_text("settings_action"), self)
        self.settings_action.triggered.connect(self.show_settings)
        self.toolbar.addAction(self.settings_action)
        
        self.themes_action = QAction(self.text_manager.get_text("themes_menu"), self)
        self.themes_action.triggered.connect(self.show_themes_market)
        self.toolbar.addAction(self.themes_action)
        
        self.languages_action = QAction(self.text_manager.get_text("texts_menu"), self)
        self.languages_action.triggered.connect(self.show_languages_menu)
        self.toolbar.addAction(self.languages_action)
        
        main_layout.addWidget(self.toolbar)
        
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        main_layout.addLayout(content_layout)
        
        sidebar = QVBoxLayout()
        sidebar.setSpacing(15)
        sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.addLayout(sidebar, 1)
        
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
        
        panel = QVBoxLayout()
        panel.setSpacing(15)
        panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.addLayout(panel, 2)
        
        crawl_group = QGroupBox(self.text_manager.get_text("crawling_queue_title"))
        crawl_layout = QVBoxLayout(crawl_group)
        crawl_layout.setContentsMargins(10, 10, 10, 10)
        self.crawl_list = QListWidget()
        crawl_layout.addWidget(self.crawl_list)
        panel.addWidget(crawl_group)
        
        archive_group = QGroupBox(self.text_manager.get_text("archiving_queue_title"))
        archive_layout = QVBoxLayout(archive_group)
        archive_layout.setContentsMargins(10, 10, 10, 10)
        self.archive_list = QListWidget()
        archive_layout.addWidget(self.archive_list)
        panel.addWidget(archive_group)
        
        self.update_proxy_display()
        self.apply_theme()

    def show_themes_market(self):
        dialog = ThemeMarketDialog(self.theme_manager, self.current_theme, self)
        dialog.exec()

    def show_languages_menu(self):
        menu = QMenu(self)
        for text in self.text_manager.available_texts:
            action = menu.addAction(text.capitalize())
            action.triggered.connect(lambda checked, t=text: self.set_language(t))
        menu.exec(self.toolbar.widgetForAction(self.languages_action).mapToGlobal(
            self.toolbar.widgetForAction(self.languages_action).rect().bottomLeft()))

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
        self.setWindowTitle(self.text_manager.get_text("window_title"))
        self.settings_action.setText(self.text_manager.get_text("settings_action"))
        self.themes_action.setText(self.text_manager.get_text("themes_menu"))
        self.languages_action.setText(self.text_manager.get_text("texts_menu"))
        
        for group in self.findChildren(QGroupBox):
            object_name = group.objectName()
            if object_name == "url_group":
                group.setTitle(self.text_manager.get_text("url_input_title"))
            elif object_name == "proxy_group":
                group.setTitle(self.text_manager.get_text("proxy_config_title"))
            elif object_name == "stats_group":
                group.setTitle(self.text_manager.get_text("progress_stats_title"))
            elif object_name == "crawl_group":
                group.setTitle(self.text_manager.get_text("crawling_queue_title"))
            elif object_name == "archive_group":
                group.setTitle(self.text_manager.get_text("archiving_queue_title"))
        
        self.add_url_btn.setText(self.text_manager.get_text("add_url_btn"))
        self.start_btn.setText(self.text_manager.get_text("start_btn"))
        self.pause_btn.setText(self.text_manager.get_text("pause_btn"))
        self.resume_btn.setText(self.text_manager.get_text("resume_btn"))
        self.stop_btn.setText(self.text_manager.get_text("stop_btn"))
        self.save_proxy_btn.setText(self.text_manager.get_text("save_proxy_btn"))
        self.clear_proxy_btn.setText(self.text_manager.get_text("clear_proxy_btn"))
        
        self.url_combo.lineEdit().setPlaceholderText(self.text_manager.get_text("url_placeholder"))
        self.proxy_text.setPlaceholderText(self.text_manager.get_text("proxy_placeholder"))
        
        for label in self.findChildren(QLabel):
            if "proxy_label" in label.objectName():
                label.setText(self.text_manager.get_text("proxy_label"))
            elif "archiving_progress_label" in label.objectName():
                label.setText(self.text_manager.get_text("archiving_progress_label"))

    def add_url(self):
        urls_input = self.url_combo.currentText().strip()
        if not urls_input:
            return
        
        urls = [url.strip() for url in urls_input.split(',') if url.strip()]
        added_urls = []
        
        for url in urls:
            if "://" not in url:
                url = "http://" + url
            
            # Check if URL already exists in the list
            if not any(self.url_list.item(i).text() == url for i in range(self.url_list.count())):
                self.url_list.addItem(url)
                added_urls.append(url)
        
        # Update recent URLs
        recent_urls = SETTINGS.get("recent_urls", [])
        for url in added_urls:
            if url in recent_urls:
                recent_urls.remove(url)
            recent_urls.insert(0, url)
        
        SETTINGS["recent_urls"] = recent_urls[:10]
        save_settings()
        
        self.url_combo.clear()
        self.url_combo.addItems(recent_urls)
        self.url_combo.setCurrentText("")
        
        # Add URLs to runng coordinator
        if self.is_running and self.coordinator and added_urls:
            try:
                for url in added_urls:
                    self.coordinator.add_url_live(url)
                log_message("INFO", f"Added URLs while running: {added_urls}", debug_only=False)
            except Exception as e:
                log_message("ERROR", f"Failed to add URLs: {str(e)}", debug_only=False)

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
        
        self.worker_thread = threading.Thread(target=self.coordinator.run, daemon=True)
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