from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#e8f4f8"
# window_text = "#3a506b"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "8pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#e8f4f8"
# group_border_color = "#d0e0e8"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#3a506b"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#ffffff"
# input_text = "#3a506b"
# input_border_color = "#b8cfe3"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#c5d8e8"
# input_selection_text = "#3a506b"
# input_placeholder = "#a0b0c0"

# --- Buttons ---
# button_bg = "#d8e8f0"
# button_text = "#3a506b"
# button_border_color = "#b8cfe3"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "80px"
# button_min_height = "30px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#c8d8e8"
# button_hover_border = "#5b9bd5"
# button_pressed_bg = "#b8c8d8"
# button_pressed_border = "#5b9bd5"
# button_disabled_bg = "#e8f4f8"
# button_disabled_text = "#a0b0c0"
# button_disabled_border = "#b8cfe3"

# --- Menu Bar ---
# menubar_bg = "#d8e8f0"
# menubar_text = "#3a506b"
# menubar_border = "#b8cfe3"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#c8d8e8"
# menubar_item_bg_selected = "#c8d8e8"
# menubar_item_text = "#3a506b"
# menubar_item_text_hover = "#3a506b"
# menubar_item_text_selected = "#3a506b"

# --- Dropdown Menus ---
# menu_bg = "#ffffff"
# menu_border = "#b8cfe3"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#c8d8e8"
# menu_item_bg_selected = "#c8d8e8"
# menu_item_text = "#3a506b"
# menu_item_text_hover = "#3a506b"
# menu_item_text_selected = "#3a506b"
# menu_separator_color = "#b8cfe3"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#e8f4f8"
# scrollbar_border = "#b8cfe3"
# scrollbar_handle_bg = "#c0d8e8"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#b0c8d8"
# scrollbar_handle_pressed_bg = "#a0b8c8"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#e8f4f8"
# progressbar_border = "#b8cfe3"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#5b9bd5"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#ffffff"
# tooltip_text = "#3a506b"
# tooltip_border = "#b8cfe3"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#ffffff"
# checkbox_border = "#b8cfe3"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#5b9bd5"
# checkbox_checked_border = "#5b9bd5"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#e8f4f8"
# slider_groove_border = "#b8cfe3"
# slider_handle_bg = "#5b9bd5"
# slider_handle_border = "#4a8bc4"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(232, 244, 248))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(58, 80, 107))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(232, 244, 248))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(58, 80, 107))
    palette.setColor(QPalette.ColorRole.Text, QColor(58, 80, 107))
    palette.setColor(QPalette.ColorRole.Button, QColor(216, 232, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(58, 80, 107))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(91, 155, 213))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(91, 155, 213))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(160, 176, 192))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 8pt;
    color: #3a506b;
    background-color: #e8f4f8;
}

QGroupBox { 
    border: 2px solid #d0e0e8;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: #e8f4f8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #3a506b;
    font-weight: bold;
}

QListWidget, QTextEdit, QLineEdit {
    background-color: #ffffff;
    color: #3a506b;
    border: 1px solid #b8cfe3;
    border-radius: 4px;
    padding: 0px;
    selection-background-color: #c5d8e8;
    selection-color: #3a506b;
}

QPushButton {
    background-color: #d8e8f0;
    color: #3a506b;
    border: 1px solid #b8cfe3;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
    max-width: 80px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton:hover {
    background-color: #c8d8e8;
    border-color: #5b9bd5;
}

QPushButton:pressed {
    background-color: #b8c8d8;
}

QPushButton:disabled {
    color: #a0b0c0;
    background-color: #e8f4f8;
}

#control_container {
    background-color: transparent;
}

QMenuBar {
    background-color: #d8e8f0;
    color: #3a506b;
    border-bottom: 1px solid #b8cfe3;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #c8d8e8;
}

QMenu {
    background-color: #ffffff;
    color: #3a506b;
    border: 1px solid #b8cfe3;
}

QMenu::item:selected {
    background-color: #c8d8e8;
}

QScrollBar:vertical {
    border: 1px solid #b8cfe3;
    background: #e8f4f8;
    width: 15px;
    margin: 0;
}

QScrollBar:horizontal {
    border: 1px solid #b8cfe3;
    background: #e8f4f8;
    height: 30px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #c0d8e8;
    min-height: 40px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background: #c0d8e8;
    min-width: 20px;
    border-radius: 7px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

QProgressBar {
    border: 1px solid #b8cfe3;
    border-radius: 4px;
    text-align: center;
    background-color: #e8f4f8;
}

QProgressBar::chunk {
    background-color: #5b9bd5;
    border-radius: 0px;
}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)