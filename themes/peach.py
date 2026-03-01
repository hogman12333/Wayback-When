from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#ffe8d8"
# window_text = "#5a4030"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "8pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#ffe8d8"
# group_border_color = "#e8d0c0"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#5a4030"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#ffffff"
# input_text = "#5a4030"
# input_border_color = "#d8c0b0"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#e8d0c0"
# input_selection_text = "#5a4030"
# input_placeholder = "#a09080"

# --- Buttons ---
# button_bg = "#f8d8c8"
# button_text = "#5a4030"
# button_border_color = "#d8c0b0"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "80px"
# button_min_height = "30px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#f0c8b8"
# button_hover_border = "#d48060"
# button_pressed_bg = "#e8b8a8"
# button_pressed_border = "#d48060"
# button_disabled_bg = "#ffe8d8"
# button_disabled_text = "#a09080"
# button_disabled_border = "#d8c0b0"

# --- Menu Bar ---
# menubar_bg = "#f8d8c8"
# menubar_text = "#5a4030"
# menubar_border = "#d8c0b0"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#f0c8b8"
# menubar_item_bg_selected = "#f0c8b8"
# menubar_item_text = "#5a4030"
# menubar_item_text_hover = "#5a4030"
# menubar_item_text_selected = "#5a4030"

# --- Dropdown Menus ---
# menu_bg = "#ffffff"
# menu_border = "#d8c0b0"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#f0c8b8"
# menu_item_bg_selected = "#f0c8b8"
# menu_item_text = "#5a4030"
# menu_item_text_hover = "#5a4030"
# menu_item_text_selected = "#5a4030"
# menu_separator_color = "#d8c0b0"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#ffe8d8"
# scrollbar_border = "#d8c0b0"
# scrollbar_handle_bg = "#f0c8b8"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#e8b8a8"
# scrollbar_handle_pressed_bg = "#d8a898"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#ffe8d8"
# progressbar_border = "#d8c0b0"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#d48060"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#ffffff"
# tooltip_text = "#5a4030"
# tooltip_border = "#d8c0b0"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#ffffff"
# checkbox_border = "#d8c0b0"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#d48060"
# checkbox_checked_border = "#d48060"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#ffe8d8"
# slider_groove_border = "#d8c0b0"
# slider_handle_bg = "#d48060"
# slider_handle_border = "#c47050"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(255, 232, 216))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(90, 64, 48))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(255, 232, 216))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(90, 64, 48))
    palette.setColor(QPalette.ColorRole.Text, QColor(90, 64, 48))
    palette.setColor(QPalette.ColorRole.Button, QColor(248, 216, 200))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(90, 64, 48))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(212, 128, 96))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(212, 128, 96))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(160, 144, 128))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 8pt;
    color: #5a4030;
    background-color: #ffe8d8;
}

QGroupBox { 
    border: 2px solid #e8d0c0;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: #ffe8d8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #5a4030;
    font-weight: bold;
}

QListWidget, QTextEdit, QLineEdit {
    background-color: #ffffff;
    color: #5a4030;
    border: 1px solid #d8c0b0;
    border-radius: 4px;
    padding: 0px;
    selection-background-color: #e8d0c0;
    selection-color: #5a4030;
}

QPushButton {
    background-color: #f8d8c8;
    color: #5a4030;
    border: 1px solid #d8c0b0;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
    max-width: 80px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton:hover {
    background-color: #f0c8b8;
    border-color: #d48060;
}

QPushButton:pressed {
    background-color: #e8b8a8;
}

QPushButton:disabled {
    color: #a09080;
    background-color: #ffe8d8;
}

#control_container {
    background-color: transparent;
}

QMenuBar {
    background-color: #f8d8c8;
    color: #5a4030;
    border-bottom: 1px solid #d8c0b0;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #f0c8b8;
}

QMenu {
    background-color: #ffffff;
    color: #5a4030;
    border: 1px solid #d8c0b0;
}

QMenu::item:selected {
    background-color: #f0c8b8;
}

QScrollBar:vertical {
    border: 1px solid #d8c0b0;
    background: #ffe8d8;
    width: 15px;
    margin: 0;
}

QScrollBar:horizontal {
    border: 1px solid #d8c0b0;
    background: #ffe8d8;
    height: 30px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #f0c8b8;
    min-height: 40px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background: #f0c8b8;
    min-width: 20px;
    border-radius: 7px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

QProgressBar {
    border: 1px solid #d8c0b0;
    border-radius: 4px;
    text-align: center;
    background-color: #ffe8d8;
}

QProgressBar::chunk {
    background-color: #d48060;
    border-radius: 0px;
}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)