from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#1e1e2e"
# window_text = "#cdd6f4"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "11pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#1e1e2e"
# group_border_color = "#181825"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#bac2de"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#313244"
# input_text = "#cdd6f4"
# input_border_color = "#45475a"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#585b70"
# input_selection_text = "#cdd6f4"
# input_placeholder = "#a0a0a0"

# --- Buttons ---
# button_bg = "#45475a"
# button_text = "#cdd6f4"
# button_border_color = "#585b70"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "120px"
# button_min_height = "40px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#585b70"
# button_hover_border = "#89b4fa"
# button_pressed_bg = "#1e1e2e"
# button_pressed_border = "#89b4fa"
# button_disabled_bg = "#313244"
# button_disabled_text = "#6c7086"
# button_disabled_border = "#585b70"

# --- Menu Bar ---
# menubar_bg = "#181825"
# menubar_text = "#cdd6f4"
# menubar_border = "#45475a"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#45475a"
# menubar_item_bg_selected = "#45475a"
# menubar_item_text = "#cdd6f4"
# menubar_item_text_hover = "#ffffff"
# menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
# menu_bg = "#313244"
# menu_border = "#45475a"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#45475a"
# menu_item_bg_selected = "#45475a"
# menu_item_text = "#cdd6f4"
# menu_item_text_hover = "#ffffff"
# menu_item_text_selected = "#ffffff"
# menu_separator_color = "#45475a"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "15px"
# scrollbar_bg = "#313244"
# scrollbar_border = "#45475a"
# scrollbar_handle_bg = "#585b70"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "20px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#6c7086"
# scrollbar_handle_pressed_bg = "#7f849c"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#313244"
# progressbar_border = "#45475a"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#89b4fa"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#313244"
# tooltip_text = "#cdd6f4"
# tooltip_border = "#45475a"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#313244"
# checkbox_border = "#45475a"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#89b4fa"
# checkbox_checked_border = "#89b4fa"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#313244"
# slider_groove_border = "#45475a"
# slider_handle_bg = "#89b4fa"
# slider_handle_border = "#74c7ec"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====

def apply(app, widget):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 46))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(205, 214, 244))
    palette.setColor(QPalette.ColorRole.Base, QColor(24, 24, 37))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(30, 30, 46))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(24, 24, 37))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(205, 214, 244))
    palette.setColor(QPalette.ColorRole.Text, QColor(205, 214, 244))
    palette.setColor(QPalette.ColorRole.Button, QColor(49, 50, 68))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(205, 214, 244))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(166, 227, 161))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(137, 180, 250))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(24, 24, 37))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(127, 132, 156))

    app.setPalette(palette)

    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #cdd6f4;
        background-color: #1e1e2e;
    }

    QGroupBox { 
        border: 2px solid #181825;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #1e1e2e;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #bac2de;
        font-weight: bold;
    }

    QListWidget, QTextEdit, QLineEdit {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #45475a;
        border-radius: 4px;
        padding: 0px;
        selection-background-color: #585b70;
        selection-color: #cdd6f4;
    }

    QPushButton {
        background-color: #45475a;
        color: #cdd6f4;
        border: 1px solid #585b70;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
        min-width: 120px;
        max-width: 120px;
        min-height: 40px;
        max-height: 40px;
    }

    QPushButton:hover {
        background-color: #585b70;
        border-color: #89b4fa;
    }

    QPushButton:pressed {
        background-color: #1e1e2e;
    }

    QPushButton:disabled {
        color: #6c7086;
        background-color: #313244;
    }

    #control_container {
        background-color: transparent;
    }

    QMenuBar {
        background-color: #181825;
        color: #cdd6f4;
        border-bottom: 1px solid #45475a;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
    }

    QMenuBar::item:selected {
        background-color: #45475a;
    }

    QMenu {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #45475a;
    }

    QMenu::item:selected {
        background-color: #45475a;
    }

    QScrollBar:vertical {
        border: 1px solid #45475a;
        background: #313244;
        width: 15px;
        margin: 0;
    }

    QScrollBar:horizontal {
        border: 1px solid #45475a;
        background: #313244;
        height: 15px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: #585b70;
        min-height: 20px;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background: #585b70;
        min-width: 20px;
        border-radius: 7px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }

    QProgressBar {
        border: 1px solid #45475a;
        border-radius: 4px;
        text-align: center;
        background-color: #313244;
    }

    QProgressBar::chunk {
        background-color: #89b4fa;
        border-radius: 0px;
    }
    """)

    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)