from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#36454f"
# window_text = "#d0d8e0"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "8pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#36454f"
# group_border_color = "#2a353d"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#c0c8d0"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#2a353d"
# input_text = "#d0d8e0"
# input_border_color = "#3a454d"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#4a555d"
# input_selection_text = "white"
# input_placeholder = "#808890"

# --- Buttons ---
# button_bg = "#3a454d"
# button_text = "#d0d8e0"
# button_border_color = "#3a454d"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "80px"
# button_min_height = "30px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#4a555d"
# button_hover_border = "#5a656d"
# button_pressed_bg = "#2a353d"
# button_pressed_border = "#5a656d"
# button_disabled_bg = "#2a353d"
# button_disabled_text = "#707880"
# button_disabled_border = "#3a454d"

# --- Menu Bar ---
# menubar_bg = "#2e3a42"
# menubar_text = "#d0d8e0"
# menubar_border = "#3a454d"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#4a555d"
# menubar_item_bg_selected = "#4a555d"
# menubar_item_text = "#d0d8e0"
# menubar_item_text_hover = "#ffffff"
# menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
# menu_bg = "#2a353d"
# menu_border = "#3a454d"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#4a555d"
# menu_item_bg_selected = "#4a555d"
# menu_item_text = "#d0d8e0"
# menu_item_text_hover = "#ffffff"
# menu_item_text_selected = "#ffffff"
# menu_separator_color = "#3a454d"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#2a353d"
# scrollbar_border = "#3a454d"
# scrollbar_handle_bg = "#4a555d"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#5a656d"
# scrollbar_handle_pressed_bg = "#6a757d"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#2a353d"
# progressbar_border = "#3a454d"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#5a656d"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#2a353d"
# tooltip_text = "#d0d8e0"
# tooltip_border = "#3a454d"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#2a353d"
# checkbox_border = "#3a454d"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#5a656d"
# checkbox_checked_border = "#5a656d"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#2a353d"
# slider_groove_border = "#3a454d"
# slider_handle_bg = "#5a656d"
# slider_handle_border = "#4a555d"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(54, 69, 79))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(208, 216, 224))
    palette.setColor(QPalette.ColorRole.Base, QColor(42, 53, 61))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(54, 69, 79))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(208, 216, 224))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(208, 216, 224))
    palette.setColor(QPalette.ColorRole.Text, QColor(208, 216, 224))
    palette.setColor(QPalette.ColorRole.Button, QColor(58, 69, 77))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(208, 216, 224))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(90, 101, 109))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(90, 101, 109))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(128, 136, 144))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 8pt;
    color: #d0d8e0;
    background-color: #36454f;
}

QGroupBox { 
    border: 2px solid #2a353d;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: #36454f;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #c0c8d0;
    font-weight: bold;
}

QListWidget, QTextEdit, QLineEdit {
    background-color: #2a353d;
    color: #d0d8e0;
    border: 1px solid #3a454d;
    border-radius: 4px;
    padding: 0px;
    selection-background-color: #4a555d;
    selection-color: white;
}

QPushButton {
    background-color: #3a454d;
    color: #d0d8e0;
    border: 1px solid #3a454d;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
    max-width: 80px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton:hover {
    background-color: #4a555d;
    border-color: #5a656d;
}

QPushButton:pressed {
    background-color: #2a353d;
}

QPushButton:disabled {
    color: #707880;
    background-color: #2a353d;
}

#control_container {
    background-color: transparent;
}

QMenuBar {
    background-color: #2e3a42;
    color: #d0d8e0;
    border-bottom: 1px solid #3a454d;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #4a555d;
}

QMenu {
    background-color: #2a353d;
    color: #d0d8e0;
    border: 1px solid #3a454d;
}

QMenu::item:selected {
    background-color: #4a555d;
}

QScrollBar:vertical {
    border: 1px solid #3a454d;
    background: #2a353d;
    width: 15px;
    margin: 0;
}

QScrollBar:horizontal {
    border: 1px solid #3a454d;
    background: #2a353d;
    height: 30px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #4a555d;
    min-height: 40px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background: #4a555d;
    min-width: 20px;
    border-radius: 7px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

QProgressBar {
    border: 1px solid #3a454d;
    border-radius: 4px;
    text-align: center;
    background-color: #2a353d;
}

QProgressBar::chunk {
    background-color: #5a656d;
    border-radius: 0px;
}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)